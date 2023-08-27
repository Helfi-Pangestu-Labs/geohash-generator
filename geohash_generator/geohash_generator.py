from config import GeoHashConfig, GeoHashConfigLoader
from geohash_util import GeohashUtil
import datetime
import click

@click.group()
def geohash_generator():
    pass

@geohash_generator.command()
@click.option('--source_path', type=str, required=True, help=(
    'the source path files.'
    'ex: /Applications/Works/geohash-generator/examples/waltdisney.geojson'
))
@click.option('--min_level_precision', type=int, required=True, help=(
    'minimum level of geohash precision'
    'ex: 2'
))
@click.option('--max_level_precision', type=int, required=True, default=12, help=(
    'maximum level of geohash precision'
    'ex: 12'
))
@click.option('--file_type', type=str, required=True, help=(
    'either shapefile or geojson'
    'ex: shapefile'
))
@click.option('--output_file_name', type=str, required=True, help=(
    'Output filename'
    'ex: geohash_waltdisney_lv12'
))
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
    
@geohash_generator.command()
@click.option('--source_path', type=str, required=True, help=(
    'the client name'
    'ex: /Applications/Works/geohash-generator/examples/geohash_waltdisney.txt'
))
def geohash_to_geojson(
    source_path: str,
):
    return GeohashUtil.convert_geohash_to_geojson(source_path=source_path)

if __name__ == "__main__":
    geohash_generator()