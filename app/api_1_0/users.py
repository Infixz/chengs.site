# coding: utf-8

from __future__ import absolute_import
import time
from flask import request, jsonify
from flask.views import MethodView
from .. import db
from ..models import Role, User
from ..celery import send_email
from ..local_settings import current_env as env
from . import api


class UserAPI(MethodView):

    def get(self, user_name):
        # query user profile
        if user_name:
            user = User.query.filter_by(username=user_name).first()
            if user:
                return jsonify({
                    'user_info': {
                        'user_id': user.id,
                        'name': user.username}
                    })
            else:
                return jsonify({
                    'err_msg': 'USER NOT FOUND'}), 404
        # query users dir
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
            html_content = '<h3>Username: %s, role: %s</h3>' % \
                (username, role_name)
            t1 = time.time()
            async_r = send_email.delay(
                    env.ADMIN_EMAIL, 'reg_notify', html_content.encode('utf8'))
            print time.time() - t1
            return jsonify({
                'status': 'create sucessful',
                'async_r': str(async_r)}), 201
        else:
            return jsonify({'status': 'check your args'}), 400

    def put(self, user_name):
        return jsonify({'status': 'Unauthorized'})

    def delete(self, user_name):
        return jsonify({'status': 'Unauthorized'})


user_view = UserAPI.as_view('user_api')

api.add_url_rule(
        rule='/users/',
        defaults={'user_name': None},
        view_func=user_view,
        methods=['GET', ]
        )
api.add_url_rule(
        rule='/users/',
        view_func=user_view,
        methods=['POST', ]
        )
api.add_url_rule(
        rule='/users/<user_name>',
        view_func=user_view,
        methods=['GET', 'PUT', 'DELETE']
        )
