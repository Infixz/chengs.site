# coding: utf-8

from flask import render_template, request, url_for, flash,\
                current_app, make_response, jsonify
from flask_login import login_required, current_user
from . import chatting


@chatting.route('/index')
def index():
    return render_template('chatting/index.html')
