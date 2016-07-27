# coding: utf-8
"""
app defined here
"""

from flask import Flask
from flask import request, make_response, redirect, abort, url_for, flash
from flask import render_template

from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy

import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

App = Flask(__name__)
App.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
App.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(App)
bootstrap = Bootstrap(App)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

@App.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html')

@App.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    
@App.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@App.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #App.run(debug=True)
    pass