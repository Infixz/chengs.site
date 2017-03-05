# coding: utf-8
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask import render_template
from flask import request, session, make_response, redirect, abort, url_for, flash

from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class OpsRecord(object):
    """This class will create a usr operations record
    decorator which will save user's ip,req method,url,
    resp_status"""
    def __init__(self, ):
        print "inside myDecorator.__init__()"
        self.fn = fn
 
    def __call__(self, func):
        self.fn()
        print "inside myDecorator.__call__()"


def ops_record(module_name):
    def deco(func):
        print 'deco apart'
        print module_name
        print func.__name__
        print request.values
        print request.url
        def warpped(*argu, **argv):
            func(*argu, **argv)
        return warpped
    return deco

def deco(func):
    print 'deco apart'
    def warpped(*argu, **argv):
        func(*argu, **argv)
    return warpped

def add_html_tag(tag, *argu, **kargv):
    def deco(func):
        css_class = " class='{0}'".format(kargv['css_class'] if "css_class" in kargv else "")
        def warpped(*argu, **argv):
            return css_class + func(*argu, **argv) + "</"+tag+">"
        return warpped
    return deco

    
class Retry(object):
    """This class will create a retry decorator.
    Using is_valid to judge if wrapped function failed.
    Retry if wrapped function failed.
    Retry at most MAX_TRIES times.
    """
    MAX_TRIES = 3

    def __init__(self, is_valid=id, max_tries=3):
        self.is_valid = is_valid
        self.MAX_TRIES = max_tries

    def __call__(self, func):
        @functools.wraps(func)
        def retried_func(*args, **kwargs):
            resp = None
            tries = 0
            while tries < self.MAX_TRIES:
                try:
                    resp = func(*args, **kwargs)
                except Exception:
                    continue
                if self.is_valid(resp):
                    break
                tries += 1
            return resp
        return retried_func


retry = Retry()

@deco
@app.route('/')

def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html')

@ops_record('user_part')
@app.route('/user/', methods=['GET','POST'])
def user_index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('user_detail',name=name))
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
