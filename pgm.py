import os
import sys
from functools import wraps
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for, Response
from pymongo import MongoClient
from jinja2 import Markup

from forms import PageForm, LoginForm

if sys.version_info[0] == 3:
  from urllib.request import urlopen
else:
  from urllib import urlopen

client = MongoClient('db', 27017)
db = client.pgmdb

admin = {'admin_name': '', 'admin_password': ''}

WSApp = Flask(__name__, instance_relative_config=False)
WSApp.debug=True
WSApp.config.from_pyfile('config.py')
print(WSApp.config)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if admin['admin_name'] != WSApp.config['ADMIN_NAME'] and \
           admin['admin_password']!= WSApp.config['ADMIN_PASSWORD']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@WSApp.route('/login', methods = ['GET', 'POST'])
def login():
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    form = LoginForm(request.form)

    if request.method == 'POST':
        admin['admin_name'] = form.admin_name.data
        admin['admin_password'] = form.admin_password.data

        return redirect(url_for('edit_pages'))

    return render_template('login_template.html', menu = menu, form = form)


@WSApp.route('/', methods = ['GET'])
def index_handler():
    doc = db.static.find_one({'name': 'home'})
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    home_markup = Markup(doc['content'])
    home_title = Markup(doc['title'])
    return render_template('page_template.html', content = home_markup,
                                                 title = home_title,
                                                 menu = menu)

@WSApp.route('/Page/view/<name>', methods = ['GET'])
def page_handler(name):
    doc = db.static.find_one({'name': name})
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    page_markup = Markup(doc['content'])
    page_title = Markup(doc['title'])
    return render_template('page_template.html', content = page_markup,
                                                 title = page_title,
                                                 menu = menu)

@WSApp.route('/Target/project/<body>', methods = ['GET'])
def map_handler(body):
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    return render_template('map_template.html', body = body, menu = menu)

@WSApp.route('/Project', methods = ['GET'])
def map_all_handler():
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    return render_template('map_template.html', body = 'All', menu = menu)

@WSApp.route('/edit', methods = ['GET', 'POST'])
@admin_required
def edit_page():
    form = PageForm(request.form)
    name = request.args['page']
    doc = db.static.find_one({'name': name})
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])

    if request.method == 'POST':
        new_title = form.page_title.data
        new_content = form.page_content.data
        new_name = form.page_name.data
        db.static.update({'name':name}, {"$set": {'content': new_content,
                                                  'title': new_title,
                                                  'name': new_name}})
        return redirect(url_for('edit_pages'))

    file_title = Markup(doc['title'])
    file_markup = Markup(doc['content'])
    form.page_title.data = file_title
    form.page_name.data = name
    form.page_content.data = file_markup
    return render_template('edit.html', form = form, menu = menu)

@WSApp.route('/remove', methods = ['POST'])
@admin_required
def remove_page():
    name =  request.form['page'];
    doc = db.static.delete_one({'name': name})
    return redirect(url_for('edit_pages'))

@WSApp.route('/admin/new', methods = ['GET', 'POST'])
@admin_required
def create_page():
    form = PageForm(request.form)
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])

    if request.method == 'POST' and form.validate():
        title = form.page_title.data
        content = form.page_content.data
        name = form.page_name.data
        db.static.insert({'name':name,
                          'content': content,
                          'title': title,
                          'type': 'page'})
        return redirect(url_for('edit_pages'))

    return render_template('edit.html', form = form, menu = menu)

@WSApp.route('/admin/pages', methods = ['GET'])
@admin_required
def edit_pages():
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    entries = [entry['name'] for entry in db.static.find({})]
    return render_template('pages.html', menu = menu, entries = entries)

@WSApp.route("/Project/view/<id>")
def project_handler(id):
    return render_template('project.html', id = id, header_dict = header_dict)

@WSApp.route("/datasets/<environment>/<dataset>/<target>/<protocol>/<ident>")
def json_dataset_id(environment, dataset, target, protocol, ident):
    url = ''
    if environment == 'dev':
        url = 'http://astrocloud-dev.wr.usgs.gov/dataset/data/'
    else:
        url = 'https://astrocloud.wr.usgs.gov/dataset/data/'
    url += dataset.lower() + '/' + target.lower() + '/' + protocol.upper()
    url += '?request=getFeature&service=WFS&version=1.1.0&outputformat=application/json'
    if ident is not None:
        url += '&id=' + ident
    response = urlopen(url)
    return Response(response.read(), status=200, mimetype='application/json')

@WSApp.route("/datasets/<environment>/<dataset>/<target>/<protocol>")
def json_dataset_target(environment, dataset, target, protocol):
    return json_dataset_id (environment, dataset, target, protocol, None)

if __name__ == "__main__":
    # @TODO probably need to remove host arg for production code, but it's
    #  necessary for local testing.
    WSApp.run(host = '0.0.0.0', port = 5000, debug=True)
