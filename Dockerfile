FROM usgsastro/miniflask
ADD . /app
WORKDIR /app
RUN conda install -c conda-forge flask geojson pymongo wtforms

CMD ['python','pgm.py']
