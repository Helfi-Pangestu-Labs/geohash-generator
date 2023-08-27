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
TBD

### Convert from Shapefile to Geohash
TBD

### Convert from Geohash to Geojson
TBD

## Testing
### Shapefile
```
make run_geohash \
    source_path=/Applications/Works/geohash-generator/examples/bioretail_region.shp \
    min_level_precision=2 \
    max_level_precision=7 \
    file_type=shapefile \
    output_file_name=waltdisney_lv7
```
### Geojson
```
make run_geohash \
    source_path=/Applications/Works/geohash-generator/examples/waltdisney.geojson \
    min_level_precision=2 \
    max_level_precision=7 \
    file_type=geojson \
    output_file_name=waltdisney_lv7
```

```
make run_geohash_to_geojson \
    source_path=/Applications/Works/geohash-generator/examples/geohash_waltdisney_lv7.txt
```