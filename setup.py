from setuptools import setup, find_packages
import re

# Get version without importing, which avoids dependency issues
def get_version():
    with open("geohash_generator/version.py") as version_file:
        return re.search(
            r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""", version_file.read()
        ).group("version")

def readme():
    with open("README.md") as f:
        return f.read()

def requirements():
    with open("requirements.txt") as f:
        return f.read()

setup(
    name = "geohash-generator",
    version = get_version(),
    license="MIT",
    description="Geohash Generator is a python module that provides function for converting geojson and shapefile to geohash.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author = "Helfi Pangestu",
    author_email = "hellfipangestu@gmail.com",
    url = "https://github.com/Helfi-Pangestu-Labs/geohash-generator/",
    download_url = "https://github.com/Helfi-Pangestu-Labs/geohash-generator/archive/main.tar.gz",
    keywords = ["geohash", "geojson", "convert", "geohash-generator", "shapefile converter", "geojson converter"], # Keywords that define your package best
    install_requires=requirements(),
    packages=find_packages(),
    include_package_data=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable", # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)