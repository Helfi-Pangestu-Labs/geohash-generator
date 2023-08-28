from geohash_generator.geohash_generator import generate
import os

# Init Variable
this_script_dir = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.join(
    this_script_dir,
    'example.shp'
)
min_level_precision=2
max_level_precision=7
file_type="shapefile"

# Convert Shapefile to Geohash
convert_shapefile_to_geohash = generate(
    source_path=source_path,
    min_level_precision=min_level_precision,
    max_level_precision=max_level_precision,
    file_type=file_type,
)

# Print result
print(f"convert_shapefile_to_geohash: {convert_shapefile_to_geohash}")
