# coding: utf-8

from __future__ import absolute_import
from flask import Blueprint

blog = Blueprint('blog', __name__)

from . import views
