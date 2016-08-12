# coding: utf-8
"""
app defined here
"""

from flask import Flask
from flask import request, session, make_response, redirect, abort, url_for, flash
from flask import render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

App = Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
App.config['SECRET_KEY'] = 'secret shit'

db = SQLAlchemy(App)
bootstrap = Bootstrap(App) # 插件



@App.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html')

@App.route('/user/')
@App.route('/user/<name>')
def user(name=None):
    return render_template('user.html', name=name)
    
@App.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@App.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    App.run(debug=True, host='0.0.0.0')
