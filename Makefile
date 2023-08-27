# Use bash syntax
SHELL := /bin/bash

# validataions
_require_output_file_name:
ifndef output_file_name
	$(error output_file_name must be defined. for example: make run_geohash output_file_name=geohash_client ...)
endif

_require_source_path:
ifndef source_path
	$(error source_path must be defined. for example: make run_geohash source_path=bioretail.shp ...)
endif

_require_min_level_precision:
ifndef min_level_precision
	$(error min_level_precision must be defined. for example: make run_geohash min_level_precision=2 ...)
endif

_require_max_level_precision:
ifndef max_level_precision
	$(error max_level_precision must be defined. for example: make run_geohash max_level_precision=8 ...)
endif

_require_file_type:
ifndef file_type
	$(error file_type must be defined. for example: make run_geohash file_type=shapefile ...)
endif

# prerequisites
install_dependency:
	pip install -r requirements.txt

# test
test: test_geohash

test_geohash: test_scripts_geohash_pyflakes test_scripts_geohash_pytest_unit

test_scripts_geohash_pyflakes:
	cd geohash_generator && \
	pyflakes .

test_scripts_geohash_pytest_unit:
	export PYTHONPATH=: && \
	coverage run -m pytest --cov-config=./.coveragerc --cov-report term-missing --cov=config -vv ./tests/unit

# deploy: runs
run_geohash: _require_source_path _require_min_level_precision _require_max_level_precision _require_file_type _require_output_file_name
	cd geohash_generator && \
	export PYTHONPATH=: && \
	python3 geohash_generator.py generate \
    --source_path=${source_path} \
    --min_level_precision=${min_level_precision} \
    --max_level_precision=${max_level_precision} \
    --file_type=${file_type} \
    --output_file_name=${output_file_name}

run_geohash_to_geojson: _require_source_path
	cd geohash_generator && \
	export PYTHONPATH=: && \
	python3 geohash_generator.py geohash-to-geojson \
    --source_path=${source_path}
