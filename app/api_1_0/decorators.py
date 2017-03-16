# coding: utf-8

from functools import wraps
from flask import g, request
from .errors import forbidden
from ..models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


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
        @wraps(func)
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


def ops_record(module_name='camel'):
    """closure return a deco"""
    def deco(func):
        @wraps(func)
        def wraped_func(*args, **kwargs):
            resp = func(*args, **kwargs)
            if request.environ['REQUEST_METHOD'] == 'GET':
                return resp
            print ':module_name:', module_name  # modify ops_record
            print ':func.__name__:', func.__name__
            print ':requ_env:', request.environ
            print ':requ.values:', request.values
            print ':form2dict:', request.form.to_dict()
            return resp
        return wraped_func
    return deco
