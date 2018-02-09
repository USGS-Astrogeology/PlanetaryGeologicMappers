FROM usgsastro/miniflask
ADD . /app
ADD requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install https://github.com/cameronbwhite/Flask-CAS/archive/v1.0.1.zip
CMD ['python','pgm.py']