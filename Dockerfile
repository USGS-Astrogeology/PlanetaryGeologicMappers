FROM usgsastro/miniflask
ADD . /app
WORKDIR /app
RUN conda install flask geojson pymongo
CMD ['python','pgm.py']