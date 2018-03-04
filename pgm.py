import os
from functools import wraps
from urllib.parse import quote, unquote

from flask import Flask, abort, flash, redirect, render_template, request, url_for, Response
from pymongo import MongoClient
from jinja2 import Markup

from forms import PageForm

client = MongoClient('localhost', 27017)
print(client.database_names())
print(client.HOST)
print(client.PORT)
db = client.pgmdb

WSApp = Flask(__name__, instance_relative_config=True)
WSApp.debug=True
# WSApp.config.from_pyfile('config.py')

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

@WSApp.route('/admin/<name>', methods = ['GET', 'POST'])
def editPage(name):
    form = PageForm(request.form)
    doc = db.static.find_one({'name': name})
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])

    if request.method == 'POST':
        new_title = form.page_title.data
        new_content = form.page_content.data
        new_name = form.page_name.data
        db.static.update({'name':name}, {"$set": {'content': new_content,
                                                  'title': new_title,
                                                  'name': new_name}})
        return redirect(url_for('editPages'))

    file_title = Markup(doc['title'])
    file_markup = Markup(doc['content'])
    form.page_title.data = file_title
    form.page_name.data = name
    form.page_content.data = file_markup
    return render_template('edit.html', form = form, menu = menu)

@WSApp.route('/remove', methods = ['POST'])
def removePage():
    name =  request.form['page'];
    doc = db.static.delete_one({'name': name})
    return redirect(url_for('editPages'))

@WSApp.route('/admin/new', methods = ['GET', 'POST'])
def createPage():
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
        return redirect(url_for('editPages'))

    return render_template('edit.html', form = form, menu = menu)

@WSApp.route('/admin/pages', methods = ['GET'])
def editPages():
    menu = Markup(db.static.find_one({'name': 'menu'})['content'])
    entries = [entry['name'] for entry in db.static.find({})]
    return render_template('pages.html', menu = menu, entries = entries)

if __name__ == "__main__":
    # @TODO probably need to remove host arg for production code, but it's
    #  necessary for local testing.
    WSApp.run(host = '0.0.0.0', port = 5000, debug=True)
