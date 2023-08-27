import os

class GeoHashConfig:
    def __init__(
        self,
        min_level_precision: int,
        max_level_precision: int,
        source_path: str,
        output_path: str,
        state: str,
        country: str,
        district: str,
        file_type: str,
        file_list: str,
        client_name: str,
        output_file_name: str,
        is_save: bool = True,
    ):
        self.min_level_precision = min_level_precision
        self.max_level_precision = max_level_precision
        self.source_path = source_path
        self.output_path = output_path
        self.state = state
        self.country = country
        self.district = district
        self.file_type = file_type
        self.file_list = file_list
        self.client_name = client_name
        self.output_file_name = output_file_name
        self.is_save = is_save

class GeoHashConfigLoader:
    @staticmethod
    def load_config_geohash_client(
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
        output_file_name: str,
    ) -> GeoHashConfig:
        this_script_dir = os.path.dirname(os.path.realpath(__file__))
        shapefile_client_config_file_path = os.path.join(
            this_script_dir,
            'client',
            client_name,
            shapefile_client_file_name,
        )

        output_path = os.path.join(
            this_script_dir,
            'client',
            client_name,
            'result',
        )

        if not os.path.isdir(output_path): 
            # prepare client directory and configlog file
            os.mkdir(output_path)

        geohash_config: GeoHashConfig = GeoHashConfig(
            min_level_precision=min_level_precision,
            max_level_precision=max_level_precision,
            source_path=shapefile_client_config_file_path,
            output_path=output_path,
            state= None if (state == '') else state,
            country= None if (country == '') else country,
            district= None if (district == '') else district,
            file_type=file_type,
            file_list= None if (file_list == '') else file_list,
            client_name=client_name,
            output_file_name=output_file_name,
            is_save=is_save,
        )
        return geohash_config