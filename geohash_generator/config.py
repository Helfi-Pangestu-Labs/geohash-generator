class GeoHashConfig:
    def __init__(
        self,
        min_level_precision: int,
        max_level_precision: int,
        source_path: str,
        file_type: str,
    ):
        """
        Initialize a GeoHashConfig instance.

        :param min_level_precision: Minimum level of geohash precision.
        :param max_level_precision: Maximum level of geohash precision.
        :param source_path: Path to the input data file.
        :param file_type: Type of the input data file (e.g., "geojson").
        """
        self.min_level_precision = min_level_precision
        self.max_level_precision = max_level_precision
        self.source_path = source_path
        self.file_type = file_type

class GeoHashConfigLoader:
    @staticmethod
    def load_config_geohash_client(
        source_path: str,
        min_level_precision: int,
        max_level_precision: int,
        file_type: str,
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
        geohash_config = GeoHashConfig(
            min_level_precision=min_level_precision,
            max_level_precision=max_level_precision,
            source_path=source_path,
            file_type=file_type,
        )
        return geohash_config
