# Use bash syntax
SHELL := /bin/bash

# prerequisites
install_dependency:
	pip install -r requirements-dev.txt

# test
test: test_geohash

test_geohash: test_scripts_geohash_pyflakes test_scripts_geohash_pytest_unit

test_scripts_geohash_pyflakes:
	cd geohash_generator && \
	pyflakes .

test_scripts_geohash_pytest_unit:
	export PYTHONPATH=: && \
	coverage run -m pytest --cov-config=./.coveragerc --cov-report term-missing --cov=config -vv ./tests/unit
