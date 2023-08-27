from geohash_generator.config import GeoHashConfig
from json import JSONEncoder
from polygon_geohasher.polygon_geohasher import polygon_to_geohashes
from geohashlite import GeoJsonHasher
from georaptor import compress
from geojson import Feature
from shapely import geometry

import concurrent.futures
import shapefile
import numpy as np
import json
class GeohashUtil:
    class NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    @staticmethod
    def convert_geohash_to_geojson(source_path: str) -> str:
        """
        Convert a list of geohashes to GeoJSON format and return as a JSON string.

        :param source_path: Path to the input geohash file.
        :return: JSON string in GeoJSON format.
        """
        geohash_reader = GeohashUtil.read_geohashes(source_path)
        
        converter = GeoJsonHasher()
        converter.geohash_codes = geohash_reader
        converter.decode_geohash(multipolygon=True)
        convert_result = converter.geojson

        geometry = convert_result['features'][0]['geometry']
        coordinates_arr = np.asarray(geometry['coordinates'])
        geometry_type = geometry['type']
        
        geojson_data = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": geometry_type,
                    "coordinates": coordinates_arr.tolist()
                }
            }]
        }

        json_object = json.dumps(geojson_data, cls=GeohashUtil.NumpyArrayEncoder)

        return json_object
    
    @staticmethod
    def read_geohashes(source_path: str) -> list:
        """
        Read geohashes from the source file.

        :param source_path: Path to the source geohash file.
        :return: List of geohashes.
        """
        with open(source_path) as f:
            lines = f.readlines()
        geohash_reader = [line[:-1] for line in lines]
        return geohash_reader

    @staticmethod
    def read_shapefile(source_path: str) -> dict:
        """
        Read and parse a shapefile and return shape records.

        :param source_path: Path to the shapefile file.
        :return: Dictionary containing shapefile records.
        """
        shapefile_reader = shapefile.Reader(source_path)
        shape_records = shapefile_reader.shapeRecords()  # Get all shape records
        
        result = {
            'shape_records': shape_records,
            'num_records': len(shape_records),
            'shape_type': shapefile_reader.shapeTypeName,
        }
        
        return result

    # Reads in geojson file and returns geojson features and the length of the shape
    @staticmethod
    def geojson_reader(source_path: str):
        """
        Read and parse GeoJSON data from a file.

        :param source_path: Path to the GeoJSON file.
        :return: List of GeoJSON features.
        """
        with open(source_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)
            features = geojson_data.get('features', [])
            return features

    @staticmethod
    def convert_geohash(coordinate, min_level_precision, max_level_precision):
        """
        Convert a coordinate to a set of refined geohashes within the given precision range.

        :param coordinate: Coordinate to convert.
        :param min_level_precision: Minimum level of geohash precision.
        :param max_level_precision: Maximum level of geohash precision.
        :return: Set of refined geohashes within the precision range.
        """
        geohash_set = set()

        # Create a Shapely Polygon from the coordinate
        polygon = geometry.Polygon(coordinate)

        # Get outer geohashes
        # inner=False: geohashes that overlap outside the polygon shape WILL be included
        # inner=True:  geohashes that overlap outside the polygon shape WILL NOT be included
        outer_geohash = set(polygon_to_geohashes(polygon, max_level_precision, inner=False))

        # Compress geohashes to the desired precision range
        refined_geohash = set(compress(outer_geohash, min_level_precision, max_level_precision))

        # Add refined geohashes to the set
        geohash_set.update(refined_geohash)

        return geohash_set
    
    @staticmethod
    def convert_geometry_to_geojson(shapely_geometry):
        """
        Convert Shapely geometry to GeoJSON format.

        :param shapely_geometry: Shapely geometry object.
        :return: GeoJSON-compatible geometry.
        """
        # Convert Shapely geometry to GeoJSON format
        return shapely_geometry.__geo_interface__

    @staticmethod
    def shapefile_type_processing(geohash_config: GeoHashConfig) -> set:
        """
        Process a shapefile type from the client and extract geohashes.

        :param geohash_config: GeoHashConfig object containing configuration parameters.
        :return: Set of extracted geohashes.
        """
        geohash_set = set()
        features = []

        # Read shapefile records
        shapefile_records = GeohashUtil.read_shapefile(geohash_config.source_path)

        # Loop through each shape and extract geohashes
        for i, feature in enumerate(shapefile_records['records']):
            print('At shape: {i} \n'.format(i=i))

            # Convert Shapely geometry to GeoJSON
            geojson_feature = GeohashUtil.convert_geometry_to_geojson(feature.shape)
            
            # Add to GeoJSON features list
            features.append(Feature(geometry=geojson_feature, properties={}))
            
            # Extract and add geohashes to the set
            geohashes = GeohashUtil.extract_geohashes(
                geometry=geojson_feature,
                min_level_precision=geohash_config.min_level_precision,
                max_level_precision=geohash_config.max_level_precision,
            )
            geohash_set.update(geohashes)

        return geohash_set

    @staticmethod
    def geojson_type_processing(geohash_config: GeoHashConfig) -> set:
        """
        Process GeoJSON data and extract geohashes within specified precision levels.

        :param geohash_config: GeoHashConfig object containing configuration parameters.
        :return: A set of extracted geohashes.
        """
        geohash_set = set()

        # Read GeoJSON features
        geojson_features_list = GeohashUtil.geojson_reader(geohash_config.source_path)

        # Iterate through each feature and extract geohashes
        for feature in geojson_features_list:
            geometry = feature.get('geometry')
            geohashes = GeohashUtil.extract_geohashes(
                    geometry=geometry,
                    min_level_precision=geohash_config.min_level_precision,
                    max_level_precision=geohash_config.max_level_precision,
                )
            geohash_set.update(geohashes)

        return geohash_set

    @staticmethod
    def extract_geohashes(geometry: dict, min_level_precision: int, max_level_precision: int) -> set:
        """
        Extract geohashes from a GeoJSON geometry.

        :param geometry: Geometry dictionary from GeoJSON feature.
        :param min_level_precision: Minimum level of geohash precision.
        :param max_level_precision: Maximum level of geohash precision.
        :return: Set of extracted geohashes.
        """

        # Get coordinates list from geojson feature
        coordinates_list = geometry['coordinates']
        multiparts = len(coordinates_list)

        # Use a thread pool for concurrent geohash conversion
        num_thread_pool = 20
        with concurrent.futures.ThreadPoolExecutor(num_thread_pool) as executor:
            futures = []
            for part in range(multiparts):
                # Handle edge cases for non-standard shapefile/geojson features
                if multiparts == 2:
                    if isinstance(coordinates_list[part], list):
                        coordinate = coordinates_list[part][0]
                    else:
                        coordinate = coordinates_list[part]
                elif geometry['type'] == 'Polygon' and multiparts == 2:
                    coordinate = coordinates_list[part]
                elif multiparts > 1:
                    if isinstance(coordinates_list[part], list):
                        coordinate = coordinates_list[part][0]
                    else:
                        coordinate = coordinates_list[part]
                else:
                    coordinate = coordinates_list[part]

                future = executor.submit(
                    GeohashUtil.convert_geohash,
                    coordinate,
                    min_level_precision,
                    max_level_precision
                )
                futures.append(future)

            # Collect results from futures
            geohashes = set()
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    geohashes.update(result)
                except Exception as e:
                    print(f"Error occurred: {e}")
            
            return geohashes
