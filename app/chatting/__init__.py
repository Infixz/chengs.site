# coding: utf-8

from __future__ import absolute_import
from flask import Blueprint

chatting = Blueprint('chatting', __name__)

from . import views
