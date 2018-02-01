import os
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for, Response
from pymongo import MongoClient

client = MongoClient(
  os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.pgmdb

WSApp = Flask(__name__, instance_relative_config=True)
WSApp.debug=True
WSApp.config.from_pyfile('config.py')

@WSApp.route("/")
def indexHandler():
  # TBD - still need to create home.html template
  return render_template('home.html', metadata=metadata)

if __name__ == "__main__":
  # @@TODO probably need to remove host arg for production code, but it's
  #  necessary for local testing.
  WSApp.run(host='0.0.0.0',debug=True)
