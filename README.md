# PlanetaryGeologicMappers

The web site for the planetary geologic mappers (PGM).  The website includes static content
with resources for mappers and current status of mapping projects including GIS footprints.

This project is the conversion of the website to use Python/Flask as the web application container.

## Creating the runtime environment

To run the web services, first create a Python 2.7 conda environment::

    > conda create -p /path/to/build/env python=2.7

Then activate the environment and install the required modules::

    > source active /path/to/build/env
    > conda install -c conda-forge -y flask flask-sqlalchemy geoalchemy2 gdal shapely geojson psycopg2

Then, run the web application::

    > source active /path/to/build/env
