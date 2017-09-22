# coding: utf-8

from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
                    not request.accept_mimetypes.accept_html:
        resp = jsonify({"error": "forbidden"})
        resp.status_code = 403
        return resp
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
                    not request.accept_mimetypes.accept_html:
        resp = jsonify({"error": "not found"})
        resp.status_code = 404
        return resp
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
                    not request.accept_mimetypes.accept_html:
        resp = jsonify({"error": "internal server error"})
        resp.status_code = 500
        return resp
    return render_template('500.html'), 500
