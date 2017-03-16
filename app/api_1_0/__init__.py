# coding: utf-8

from __future__ import absolute_import
from flask import Blueprint

api = Blueprint('api', __name__)

from . import users
