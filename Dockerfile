FROM usgsastro/miniflask
ADD . /app
ADD requirements.txt /app
WORKDIR /app
RUN conda install flask geojson pymongo
CMD ['python','pgm.py']