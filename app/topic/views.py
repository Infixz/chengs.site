# coding: utf-8

from flask import render_template, request, url_for, flash,\
                current_app, make_response, jsonify, redirect
from flask_login import login_required, current_user
from . import topic  # 此处 . 代表 todo_list包 而非 __init__.py
from forms import TopicForm


@topic.route('/index')
def index():
    return render_template('topic/index.html')


@topic.route('/show_all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('topic.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@topic.route('/show_followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('topic.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp
