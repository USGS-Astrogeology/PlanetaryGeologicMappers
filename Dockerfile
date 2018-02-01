FROM usgsastro/miniflask
ADD . /app
WORKDIR /app
RUN conda install -c conda-forge flask flask-sqlalchemy geoalchemy2 gdal shapely geojson psycopg2 pymongo

CMD ['python','pgm.py']