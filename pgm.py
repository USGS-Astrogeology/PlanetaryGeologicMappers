import os
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for, Response
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pgmdb

#WSApp = Flask(__name__, instance_relative_config=True)
#WSApp.debug=True
#WSApp.config.from_pyfile('config.py')
WSApp = Flask(__name__)

map_list = ['Venus', 'Mars', 'Mercury', 'Moon', 'Europa',
            'Enceladus', 'Ganymede', 'Io', 'Vesta']
page_list = ['Guidelines', 'Resources', 'Meetings', 'Milestones', 'FAQ']
header_dict = {'maps': map_list, 'pages': page_list}

@WSApp.route("/")
def indexHandler():
  return render_template('page_template.html', content = 'home.html', header_dict = header_dict)

@WSApp.route("/Page/view/<page>")
def pageHandler(page):
  content = page + '.html'
  return render_template('page_template.html', content = content, header_dict = header_dict)

@WSApp.route("/Target/project/<body>")
def mapHandler(body):
  return render_template('map_template.html', body = body, header_dict = header_dict)

@WSApp.route("/Project")
def mapAllHandler():
    return render_template('map_template.html', body = 'All', header_dict = header_dict)

@WSApp.route("/Project/view/<id>")
def projectHandler(id):
    return render_template('project.html', id = id, header_dict = header_dict)

if __name__ == "__main__":
  # @TODO probably need to remove host arg for production code, but it's
  #  necessary for local testing.
  WSApp.run(host='0.0.0.0', debug=True)
