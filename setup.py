import os

from setuptools import setup, find_packages

NAME = "aio_geojson_planefinderlocal"
AUTHOR = "Mark Kuchel"
AUTHOR_EMAIL = "mark@kuchel.net"
DESCRIPTION = "An async GeoJSON client library for planes using information from a Planefinder local server."
URL = "https://github.com/kuchel77/python-aio-geojson-planefinderlocal"

REQUIRES = [
    'aio_geojson_client>=0.11',
    'aiohttp>=3.5.4',
    'pytz>=2019.01',
]


with open("README.md", "r") as fh:
    long_description = fh.read()

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = {}
with open(os.path.join(HERE, NAME, "__version__.py")) as f:
    exec(f.read(), VERSION)  # pylint: disable=exec-used

setup(
    name=NAME,
    version=VERSION["__version__"],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES
)
