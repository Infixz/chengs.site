# coding: utf-8

from flask import render_template, request, url_for, flash,\
                current_app, make_response, jsonify
from flask_login import login_required, current_user
from . import topic  # 此处 . 代表 todo_list包 而非 __init__.py


@topic.route('/index')
def index():
    return render_template('topic/index.html')
