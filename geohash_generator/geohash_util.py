from config import GeoHashConfig
from polygon_geohasher.polygon_geohasher import polygon_to_geohashes
from georaptor import compress
from json import JSONEncoder
from geojson import Feature, FeatureCollection, dump
from shapely import geometry

import concurrent.futures
import geojson
import shapefile
import geohashlite
import numpy as np
import json
import os

class GeohashUtil:
    @staticmethod
    def convert_geohash_to_geojson(
        client_name: str,
        geohash_file_name: str,
    ):
        this_script_dir = os.path.dirname(os.path.realpath(__file__))
        source_path = os.path.join(
            this_script_dir,
            'client',
            client_name,
            'result',
            geohash_file_name
        )

        remove_extension = geohash_file_name.split('.')[0]
        output_path = os.path.join(
            this_script_dir,
            'client',
            client_name,
            f'{remove_extension}_convert_to_geojson.geojson'
        )
    
        # read file
        with open(source_path) as f:
            lines = f.readlines()
        geohash_reader = [line[:-1] for line in lines]
        
        converter = geohashlite.GeoJsonHasher()

        converter.geohash_codes = geohash_reader
        converter.decode_geohash(multipolygon=True)
        convert_result = converter.geojson

        geometry = convert_result['features'][0]['geometry']
        coordinates_arr = np.asarray(geometry['coordinates'])
        geometry_type = geometry['type']
        res =  {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": geometry_type,
                            "coordinates": coordinates_arr
                        }
                    }]
                }

        class NumpyArrayEncoder(JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return JSONEncoder.default(self, obj)

        json_object =json.dumps(res, cls=NumpyArrayEncoder)

        with open(output_path, 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def shapefile_reader(source_path: str) -> dict:
        """
        Reads in shapefile and returns records in an object, the length of the shape, and the shape itself
        
        Parameters
        ----------
        source_path : str
            Source path of shapefile file.
        
        Return dictionary of key: string, value: string
        """
        result = dict()
        result['shape'] = shapefile.Reader(source_path)
        result['records'] = result['shape'].shapeRecords()  # Get all records from the shape
        
        print(f"result: {result}")
        return result
    
    # Reads in geojson file and returns geojson features and the length of the shape
    @staticmethod
    def geojson_reader(source_path: str):
        """
        Reads in shapefile and returns records in an object, the length of the shape, and the shape itself
        
        Parameters
        ----------
        source_path : str
            Source path of geojson file.
        
        Return dictionary of key: string, value: string
        """
        result = dict()

        with open(source_path) as f:
            gj = geojson.load(f)
        result['gj_features'] = gj['features']

        return result

    @staticmethod
    def add_geohashes_to_set(
        geohash_set: set, 
        geojson_feature: dict, 
        min_level_precision: int, 
        max_level_precision: int): 
        """
        Given a list of coordinates, get refined set of geohashes.

        Parameters
        ----------
        geohash_set : set
            Empty initialized set
        geojson_feature : dict
            geojson object (can be extracted from shapefile or taken as is)
        min_level_precision : int
            minimum level of geohash precision
        max_level_precision : int
            maximum level of geohash precision

        Returns
        -------
        set
            a list of geohash from the location
        """
        # Get coordinates list from geojson feature
        coordinates_list = geojson_feature['coordinates'] 
        # Get number of parts from current feature
        multiparts = len(coordinates_list) 
        print('multiparts: {multiparts} \n'.format(multiparts=multiparts))

        # Loop through multiparts and create hashes for each
        for part in range(0,multiparts):
            # Handle edge cases for non-standard shapefile/geojson features
            if multiparts == 2:
                print('Two multiparts')
                if isinstance(coordinates_list[part], list):
                    coordinate = coordinates_list[part][0]
                else:
                    coordinate = coordinates_list[part]
            elif geojson_feature['type'] == 'Polygon' and multiparts == 2:
                print('Type is polygon and two multiparts')
                coordinate = coordinates_list[part]
            elif multiparts > 1:
                print('More than 1 multipart')
                if isinstance(coordinates_list[part], list):
                    coordinate = coordinates_list[part][0]
                else:
                    coordinate = coordinates_list[part]
            else:
                print('Something else')
                coordinate = coordinates_list[part]

            print(f"part: {part}")
            # Get polygon
            polygon = geometry.Polygon(coordinate)

            # Get outer geohash
            # inner=False: geohashes that overlap outside the polygon shape WILL be included
            # inner=True:  geohashes that overlap outside the polygon shape WILL NOT be included
            outer_geohash = set(polygon_to_geohashes(polygon, max_level_precision, inner=False)) 

            # # Set geohash WITHOUT compression
            # for o_hash in outer_geohash:
            #     geohash_set.add((o_hash, zip_code))

            # Get refined geohash
            refined_geohash = set(compress(outer_geohash, min_level_precision, max_level_precision))
            for x in refined_geohash:
                geohash_set.add(x)
    
    @staticmethod
    def add_geohashes_to_set_v2(
        geohash_set: set, 
        geojson_feature: dict, 
        min_level_precision: int, 
        max_level_precision: int): 
        """
        Given a list of coordinates, get refined set of geohashes.

        Parameters
        ----------
        geohash_set : set
            Empty initialized set
        geojson_feature : dict
            geojson object (can be extracted from shapefile or taken as is)
        min_level_precision : int
            minimum level of geohash precision
        max_level_precision : int
            maximum level of geohash precision

        Returns
        -------
        set
            a list of geohash from the location
        """
        # Get coordinates list from geojson feature
        coordinates_list = geojson_feature['coordinates'] 
        # Get number of parts from current feature
        multiparts = len(coordinates_list) 
        print('multiparts: {multiparts} \n'.format(multiparts=multiparts))

        # Loop through multiparts and create hashes for each
        num_thread_pool = 20
        with concurrent.futures.ThreadPoolExecutor(num_thread_pool) as executor:
            futures = []
            for part in range(0,multiparts):
                # Handle edge cases for non-standard shapefile/geojson features
                if multiparts == 2:
                    print('Two multiparts')
                    if isinstance(coordinates_list[part], list):
                        coordinate = coordinates_list[part][0]
                    else:
                        coordinate = coordinates_list[part]
                elif geojson_feature['type'] == 'Polygon' and multiparts == 2:
                    print('Type is polygon and two multiparts')
                    coordinate = coordinates_list[part]
                elif multiparts > 1:
                    print('More than 1 multipart')
                    if isinstance(coordinates_list[part], list):
                        print("isinstance always index 0")
                        coordinate = coordinates_list[part][0]
                    else:
                        print("isinstance")
                        coordinate = coordinates_list[part]
                else:
                    print('Something else')
                    coordinate = coordinates_list[part]

                print(f"coordinate: {coordinate}")
                future = executor.submit(
                    GeohashUtil.convert_geohash,
                    geohash_set,
                    coordinate,
                    min_level_precision,
                    max_level_precision
                )
                futures.append(future)

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Retrieve the result of the task
                except Exception as e:
                    print(f"Error occurred: {e}")
    
    @staticmethod
    def convert_geohash(geohash_set: set, coordinate, min_level_precision, max_level_precision):
        # Get polygon
        polygon = geometry.Polygon(coordinate)
        print(f"polygon: {polygon}")

        # Get outer geohash
        # inner=False: geohashes that overlap outside the polygon shape WILL be included
        # inner=True:  geohashes that overlap outside the polygon shape WILL NOT be included
        outer_geohash = set(polygon_to_geohashes(polygon, max_level_precision, inner=False)) 
        print(f"outer_geohash: {outer_geohash}")

        # Get refined geohash
        refined_geohash = set(compress(outer_geohash, min_level_precision, max_level_precision))
        for x in refined_geohash:
            geohash_set.add(x)

        print("Success convert to geohash")

    @staticmethod
    def write_geojson(
        features: list, 
        geohash_config: GeoHashConfig,
        ):
        """
        Write a geojson file to the path
        """
        feature_collection = FeatureCollection(features)
        geojson_file_name = f'{geohash_config.output_path}/{geohash_config.output_file_name}.geojson'
        with open(geojson_file_name, 'w') as f:
            dump(feature_collection, f)
    
    @staticmethod
    def write_geohash(
        geohash_set: set,
        geohash_config: GeoHashConfig,
        ):
        """
        Write a geohash file to the path
        """
        geohash_file_name = f'{geohash_config.output_path}/geohash_{geohash_config.output_file_name}.txt'
        print('Writing to: ', geohash_file_name)
        with open(geohash_file_name, 'w') as file_handler:
            for item in geohash_set:
                file_handler.write("{geohash}\n".format(geohash=item))
        file_handler.close()

    @staticmethod
    def shapefile_type_processing(
        geohash_config: GeoHashConfig
    ) -> dict:
        """
        Process a shapefile type from client
        Return dictionary of key: string, value: string
        """
        geohash_set = set() 
        record_index = 0
        features = []

        # Get all shapefile records 
        shapefile_records_dict = GeohashUtil.shapefile_reader(geohash_config.source_path)

        # For straightforward country geohashes
        if geohash_config.state == None and geohash_config.country == None:
            # Loop through each shape and get hashes
            for i in range(0, len(shapefile_records_dict['shape']) ):
                print('At shape: {i} \n'.format(i=i))
                # Get geometry and attributes
                feature = shapefile_records_dict['records'][i]  
                # Returns data as geojson/dictionary
                geojson_feature = feature.shape.__geo_interface__ 
                # Append to geojson features
                features.append(Feature(geometry=geojson_feature, properties={}))
                # Add hashes to geohash set
                GeohashUtil.add_geohashes_to_set(
                    geohash_set=geohash_set, 
                    geojson_feature=geojson_feature, 
                    min_level_precision=geohash_config.min_level_precision, 
                    max_level_precision=geohash_config.max_level_precision,
                    ) 

        # For state and/or country level geohashes
        elif geohash_config.state != None or geohash_config.country != None:
            # Loop through each shape to identify state or country within state
            for i in shapefile_records_dict['shape'].iterRecords():
                # For state only ( for US,CA [4], for NV [8] )
                if geohash_config.state != None and geohash_config.country == None and geohash_config.district==None:
                    if i[4] == geohash_config.state:
                        print("Found state {} at index {} ".format(geohash_config.state, record_index))
                        print(i)
                        break
                # For country within a state (for US [6])
                elif geohash_config.state != None and geohash_config.country != None and geohash_config.district==None:
                    if i[4] == geohash_config.state and i[6] == geohash_config.country:
                        print("Found state {} and country {} at index {} ".format(geohash_config.state, geohash_config.country, record_index))
                        print(i)
                        break
                # For district within country within state
                elif geohash_config.state != None and geohash_config.country != None and geohash_config.district != None:
                    if i[4] == geohash_config.state and i[6] == geohash_config.country and i[8] == geohash_config.district:
                        print("Found state {} and country {} and district {} at index {} ".format(geohash_config.state, geohash_config.country, geohash_config.district, record_index))
                        print(i)
                        break
                # Increment the index
                record_index += 1

            # Get geometry and attributes
            feature = shapefile_records_dict['records'][record_index]
            # Returns data as geojson/dictionary
            geojson_feature = feature.shape.__geo_interface__ 
            # Append to geojson features
            features.append(Feature(geometry=geojson_feature, properties={}))
            # Add hashes to geohash set
            GeohashUtil.add_geohashes_to_set(
                geohash_set=geohash_set, 
                geojson_feature=geojson_feature, 
                min_level_precision=geohash_config.min_level_precision, 
                max_level_precision=geohash_config.max_level_precision,
            ) 

        # Write to geojson
        GeohashUtil.write_geojson(features=features, geohash_config=geohash_config)

        if geohash_config.is_save == True:
            GeohashUtil.write_geohash(
                geohash_set=geohash_set,
                geohash_config=geohash_config,
            )
    
    @staticmethod
    def geojson_type_processing(
        geohash_config: GeoHashConfig
    )-> dict:
        """
        Process a geojson type from client
        Return dictionary of key: string, value: string
        """
        geohash_set = set() 

        # Get geojson feature and number of features
        geojson_features_dict = GeohashUtil.geojson_reader(geohash_config.source_path)
        # For straightforward country geohashes
        if geohash_config.state == None and geohash_config.country == None:
            # Loop through each shape and get hashes
            for i in range(0, len(geojson_features_dict['gj_features'])):
                print('At geojson object: {i} \n'.format(i=i))
                # Locate geojson feature
                geojson_feature = geojson_features_dict['gj_features'][i]['geometry']
                # Add hashes to geohash set
                GeohashUtil.add_geohashes_to_set(
                    geohash_set=geohash_set, 
                    geojson_feature=geojson_feature, 
                    min_level_precision=geohash_config.min_level_precision, 
                    max_level_precision=geohash_config.max_level_precision,
                )

        if geohash_config.is_save == True:
            GeohashUtil.write_geohash(
                geohash_set=geohash_set,
                geohash_config=geohash_config,
            )
    
    @staticmethod
    def geojson_type_processing_v2(
        geohash_config: GeoHashConfig
    )-> dict:
        """
        Process a geojson type from client
        Return dictionary of key: string, value: string
        """
        geohash_set = set() 

        # Get geojson feature and number of features
        geojson_features_dict = GeohashUtil.geojson_reader(geohash_config.source_path)
        # For straightforward country geohashes
        if geohash_config.state == None and geohash_config.country == None:
            # Loop through each shape and get hashes
            for i in range(0, len(geojson_features_dict['gj_features'])):
                print('At geojson object: {i} \n'.format(i=i))
                # Locate geojson feature
                geojson_feature = geojson_features_dict['gj_features'][i]['geometry']
                # Add hashes to geohash set
                GeohashUtil.add_geohashes_to_set_v2(
                    geohash_set=geohash_set, 
                    geojson_feature=geojson_feature, 
                    min_level_precision=geohash_config.min_level_precision, 
                    max_level_precision=geohash_config.max_level_precision,
                )

        if geohash_config.is_save == True:
            GeohashUtil.write_geohash(
                geohash_set=geohash_set,
                geohash_config=geohash_config,
            )

    @staticmethod
    def dedup_geohash_to_max_precision_level_2(
        client_name: str,
        geohash_file_name: str,
    ):
        """
        Dedup Geohash to max precision level 2
        """
        this_script_dir = os.path.dirname(os.path.realpath(__file__))

        split_geohash_file_name = geohash_file_name.split(',')
        geohash_reader_list = []

        print(f'split_geohash_file_name: {split_geohash_file_name}')

        for geohash_file_name in split_geohash_file_name:
            print(f'current geohash_file_name: {geohash_file_name}')
            source_path = os.path.join(
                this_script_dir,
                'client',
                client_name,
                'result',
                geohash_file_name
            )
        
            # read file
            with open(source_path) as f:
                lines = f.readlines()
            geohash_reader = [line[:-1] for line in lines]

            geohash_reader_list.append(geohash_reader)

        # dedup
        result = []
        for index in range(len(geohash_reader_list)):
            for geohash_reader in geohash_reader_list[index]:
                substring_first_two_char = geohash_reader[:2]
                if substring_first_two_char not in result:
                    result.append(substring_first_two_char)
        
        print(f'result: {result}')
        print('Successfully dedup and get max precision level 2. And goto Restore Data and put that value to the geo2')