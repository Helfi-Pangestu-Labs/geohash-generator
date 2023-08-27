import os
class GeoHashConfig:
    def __init__(
        self,
        min_level_precision: int,
        max_level_precision: int,
        source_path: str,
        output_path: str,
        file_type: str,
        output_file_name: str,
    ):
        """
        Initialize a GeoHashConfig instance.

        :param min_level_precision: Minimum level of geohash precision.
        :param max_level_precision: Maximum level of geohash precision.
        :param source_path: Path to the input data file.
        :param output_path: Path to the output directory.
        :param file_type: Type of the input data file (e.g., "geojson").
        :param output_file_name: Name of the output file (without extension).
        """
        self.min_level_precision = min_level_precision
        self.max_level_precision = max_level_precision
        self.source_path = source_path
        self.output_path = output_path
        self.file_type = file_type
        self.output_file_name = output_file_name

class GeoHashConfigLoader:
    @staticmethod
    def load_config_geohash_client(
        source_path: str,
        min_level_precision: int,
        max_level_precision: int,
        file_type: str,
        output_file_name: str,
    ) -> GeoHashConfig:
        """
        Load and create a GeoHashConfig instance for the client.

        :param source_path: Path to the input data file.
        :param min_level_precision: Minimum level of geohash precision.
        :param max_level_precision: Maximum level of geohash precision.
        :param file_type: Type of the input data file (e.g., "geojson").
        :param output_file_name: Name of the output file (without extension).
        :return: A GeoHashConfig instance.
        """
        output_path = os.path.dirname(source_path)

        geohash_config = GeoHashConfig(
            min_level_precision=min_level_precision,
            max_level_precision=max_level_precision,
            source_path=source_path,
            output_path=output_path,
            file_type=file_type,
            output_file_name=output_file_name,
        )
        return geohash_config
