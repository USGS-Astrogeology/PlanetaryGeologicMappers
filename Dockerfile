FROM usgsastro/miniflask

RUN conda install -c conda-forge flask geojson pymongo wtforms
ADD . /app
WORKDIR /app

CMD ["python", "pgm.py"]
