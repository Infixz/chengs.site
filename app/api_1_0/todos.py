# coding: utf-8

from __future__ import absolute_import
from flask import request, url_for, current_app, jsonify
from flask.views import MethodView
from .. import db
from ..models import Role, User, Todo, Permission
from . import api


class TodosAPI(MethodView):

    def get(self, user_name):
        if user_name:
            user = User.query.filter_by(username=user_name).first()
            if user:
                return jsonify({
                        'user_info': {
                                'user_id': user.id, 'name': user.username
                                }
                        })
            else:
                return jsonify({'err_msg': 'USER NOT FOUND'}), 404
        else:
            return jsonify({
                'user_list': [{'user_id': item.id, 'name': item.username} for item in User.query.all()],
                'user_count': User.query.count()
                })

    def post(self):
        username = request.form['user_name']
        role_id = request.form['role_id']
        if username and int(role_id):
            new = User(username=username, role_id=role_id)
            role_name = Role.query.filter_by(id=role_id).first().name
            db.session.add(new)
            try:
                db.session.commit()
            except Exception, e:
                db.session.rollback()
                return jsonify({'err_msg': str(e)}), 400
            return jsonify({
                'status': 'create sucessful'
                }), 201

    def put(self, user_name):
        return jsonify({'status': 'Unauthorized'})

    def delete(self, user_name):
        return jsonify({'status': 'Unauthorized'})


todos_view = TodosAPI.as_view('todos')
api.add_url_rule(
        rule='/users/',
        defaults={'user_name': None},
        view_func=todos_view,
        methods=['GET', ])
api.add_url_rule(
        rule='/users/',
        view_func=todos_view,
        methods=['POST', ])
api.add_url_rule(
        rule='/users/<user_name>',
        view_func=todos_view,
        methods=['GET', 'PUT', 'DELETE'])
