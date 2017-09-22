# coding: utf-8

from __future__ import absolute_import
from flask import Blueprint

todo_list = Blueprint('todo_list', __name__)

from . import views
