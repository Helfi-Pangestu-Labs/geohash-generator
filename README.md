# Geohash Generator
Geohash Generator is a python module that provides function for converting geojson and shapefile to geohash. 

## Feature
- [x] Convert from Geojson to Geohash
- [x] Convert from Shapefile to Geohash
- [x] Convert from Geohash to Geojson
- [ ] Do you have any idea for other feature?

## Reqruiements
- Python: 2.x, 3.x

## Installation
```
pip install geohash-generator
```

## Usage
### Convert from Geojson to Geohash
```
from geohash_generator.geohash_generator import generate
import os

# Init Variable
this_script_dir = os.path.dirname(os.path.realpath(__file__))
source_path = os.path.join(
        this_script_dir,
        'example.geojson'
    )
min_level_precision=2
max_level_precision=7
file_type="geojson"

# Convert Geojson to Geohash
convert_geojson_to_geohash = generate(
    source_path=source_path,
    min_level_precision=min_level_precision,
    max_level_precision=max_level_precision,
    file_type=file_type,
    )

# Print result
print(f"generate_geohash: {convert_geojson_to_geohash}")
```

### Convert from Shapefile to Geohash
```
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
converth_shapefile_to_geohash = generate(
    source_path=source_path,
    min_level_precision=min_level_precision,
    max_level_precision=max_level_precision,
    file_type=file_type,
    )

# Print result
print(f"generate_geohash: {converth_shapefile_to_geohash}")
```

### Convert from Geohash to Geojson
```
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
```
