from geohash_generator.config import GeoHashConfig, GeoHashConfigLoader
from geohash_generator.geohash_util import GeohashUtil
import datetime

def generate(
    source_path: str,
    min_level_precision: int,
    max_level_precision: int,
    file_type: str,
    output_file_name:str,
):
    """
    Generate geohash file based on shapefile or geojson from client config.
    """
    start_job_at = datetime.datetime.now()

    geohash_config: GeoHashConfig = GeoHashConfigLoader.load_config_geohash_client(
        source_path=source_path,
        min_level_precision=min_level_precision,
        max_level_precision=max_level_precision,
        file_type=file_type,
        output_file_name=output_file_name,
    )

    if geohash_config.file_type == 'shapefile':
        result = GeohashUtil.shapefile_type_processing(geohash_config=geohash_config)
    elif geohash_config.file_type == 'geojson' :
        result = GeohashUtil.geojson_type_processing(geohash_config=geohash_config)

    print(f'Started Job at: {start_job_at}')
    print(f'Ended Job at: {datetime.datetime.now()}')
    return result

def geohash_to_geojson(
    source_path: str,
):
    return GeohashUtil.convert_geohash_to_geojson(source_path=source_path)
