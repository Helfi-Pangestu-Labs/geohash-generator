from config import GeoHashConfig, GeoHashConfigLoader
from geohash_util import GeohashUtil
import datetime
import click

@click.group()
def geohash_generator():
    pass

@geohash_generator.command()
@click.option('--shapefile_client_file_name', type=str, required=True, help=(
    'the file name for shapefile configs in client/<client-name> folder. '
    'ex: bioretail_region.shp'
))
@click.option('--client_name', type=str, required=True, help=(
    'the client name'
    'ex: bioretail'
))
@click.option('--min_level_precision', type=int, required=True, help=(
    'minimum level of geohash precision'
    'ex: 2'
))
@click.option('--max_level_precision', type=int, required=True, default=8, help=(
    'maximum level of geohash precision'
    'ex: 8'
))
@click.option('--state', type=str, required=False, default=None, help=(
    'the state name'
    'ex: Maharashtra'
))
@click.option('--country', type=str, required=False, default=None, help=(
    'the country name'
    'ex: Greater Bombay'
))
@click.option('--district', type=str, required=False, default=None, help=(
    'the district name'
    'ex: n.a. ( 1556)'
))
@click.option('--file_type', type=str, required=True, help=(
    'either shapefile or geojson'
    'ex: shapefile'
))
@click.option('--file_list', type=str, required=False, default=None, help=(
    ' IN PROGRESS'
    'ex:  IN PROGRESS'
))
@click.option('--is_save', type=bool, required=False, default=True, help=(
    'is the result want to save. either True or False'
    'ex: true'
))
@click.option('--output_file_name', type=str, required=True, help=(
    'Output filename'
    'ex: geohash_victoria'
))
def generate(
    shapefile_client_file_name: str,
    client_name: str,
    min_level_precision: int,
    max_level_precision: int,
    state: str,
    country: str,
    district: str,
    file_type: str,
    file_list: str,
    is_save: bool,
    output_file_name:str,
):
    """
    Generate geohash file based on shapefile from client config.
    """
    start_job_at = datetime.datetime.now()

    geohash_config: GeoHashConfig = GeoHashConfigLoader.load_config_geohash_client(
        shapefile_client_file_name=shapefile_client_file_name,
        client_name=client_name,
        min_level_precision=min_level_precision,
        max_level_precision=max_level_precision,
        state=state,
        country=country,
        district=district,
        file_type=file_type,
        file_list=file_list,
        is_save=is_save,
        output_file_name=output_file_name,
    )

    if geohash_config.file_type == 'shapefile':
        GeohashUtil.shapefile_type_processing(geohash_config=geohash_config)
    elif geohash_config.file_type == 'geojson' :
        GeohashUtil.geojson_type_processing_v2(geohash_config=geohash_config)

    print(f'Started Job at: {start_job_at}')
    print(f'Ended Job at: {datetime.datetime.now()}')
    
@geohash_generator.command()
@click.option('--client_name', type=str, required=True, help=(
    'the client name'
    'ex: adxflare'
))
@click.option('--geohash_file_name', type=str, required=True, help=(
    'the file name for geohash configs in client/<client-name> folder. '
    'ex: geohash_adxflare.txt'
))
def geohash_to_geojson(
    client_name: str,
    geohash_file_name: str,
):
    GeohashUtil.convert_geohash_to_geojson(client_name=client_name,geohash_file_name=geohash_file_name)

@geohash_generator.command()
@click.option('--client_name', type=str, required=True, help=(
    'the client name'
    'ex: adxflare'
))
@click.option('--geohash_file_name', type=str, required=True, help=(
    'the file name for geohash configs in client/<client-name> folder. '
    'ex: geohash_adxflare.txt'
))
def generate_list_max_precision_level_2(
    client_name: str,
    geohash_file_name: str,
):
    GeohashUtil.dedup_geohash_to_max_precision_level_2(client_name=client_name,geohash_file_name=geohash_file_name)

if __name__ == "__main__":
    geohash_generator()