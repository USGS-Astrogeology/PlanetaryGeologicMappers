from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for, Response

WSApp = Flask(__name__, instance_relative_config=True)
WSApp.debug=True
WSApp.config.from_pyfile('config.py')

@WSApp.route("/")
def indexHandler():
  # TBD - still need to create home.html template
  return render_template('home.html', metadata=metadata)

if __name__ == "__main__":
  WSApp.run(debug=True)
