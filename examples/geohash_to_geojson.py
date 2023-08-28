from geohash_generator.geohash_generator import geohash_to_geojson
import os

# Init Variable
this_script_dir = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.join(
    this_script_dir,
    'geohash_example.txt'
)

# Convert Geohash to Geojson
convert_geohash_to_geojson = geohash_to_geojson(source_path=source_path)

# Print Result
print(f"convert_geohash_to_geojson: {convert_geohash_to_geojson}")