# coding: utf-8
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask import request, session, make_response, redirect, abort, url_for, flash
from flask import render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html')


@app.route('/user/', methods=['GET','POST'])
def user_index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('user_detail'))
    return render_template('user_index.html',name=name,form=form)

@app.route('/user/<name>')
def user_detail(name=None):
    return render_template('user.html', name=name)
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
