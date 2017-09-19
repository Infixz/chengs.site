# coding: utf-8

from flask import render_template, redirect, request, url_for, flash,\
                  current_app, make_response
from flask_login import login_required, current_user
from . import todo_list
# from .forms import PostForm
# from .. import db
# from ..models import 


@todo_list.route('/index')
@login_required
def index():
    return render_template('todo_list/index.html')
