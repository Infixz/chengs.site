# coding: utf-8

from flask import render_template, request, url_for, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user
from . import todo_list  # 此处 . 代表 todo_list包 而非 __init__.py
from ..models import Todo
from .. import db
from datetime import datetime


@todo_list.route('/index')
@login_required
def index():
    return render_template('todo_list/index.html')


class TodosAPI(MethodView):

    def get(self, todo_id):
        if todo_id:
            todo = Todo.query.get_or_404(todo_id)
            return jsonify({
                    'id': todo.id,
                    'task': todo.task,
                    'order': todo.order,
                    'done': todo.done
                    })
        todos = Todo.query.filter_by(author_id=current_user.id).all()
        if todos:
            return jsonify([{
                    'id': i.id,
                    'task': i.task,
                    'order': i.order,
                    'done': i.done} for i in todos]), 200
        return jsonify({'ERR_MSG': 'NOT FOUND'}), 404

    def post(self):
        todo_json = request.json
        todo_new = Todo(
            task=todo_json['task'],
            order=todo_json['order'],
            done=todo_json['done'],
            timestamp=datetime.utcnow(),
            author_id=current_user.id
        )
        db.session.add(todo_new)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            return jsonify({'err_msg': str(e)}), 400
        return jsonify({'status': 'create sucessful'}), 201, \
            {
                'Location': url_for(
                    'todo_list.todos_view',
                    id=todo_new.id,
                    _external=True
                )
            }

    def put(self, todo_id):
        todo_json = request.json
        todo_new = Todo(
            id=todo_json['id'],
            task=todo_json['task'],
            order=todo_json['order'],
            done=todo_json['done'],
            timestamp=datetime.utcnow(),
            author_id=current_user.id
        )
        db.session.add(todo_new)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            return jsonify({'err_msg': str(e)}), 400
        return jsonify({'status': 'create sucessful'}), 201

    def delete(self, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            return jsonify({'err_msg': str(e)}), 400
        return jsonify({'status': 'no content'}), 204


todos_view = TodosAPI.as_view('todos_view')
todo_list.add_url_rule(
        rule='/todos/',
        defaults={'todo_id': None},
        view_func=todos_view,
        methods=['GET', ])
todo_list.add_url_rule(
        rule='/todos/',
        view_func=todos_view,
        methods=['POST', ])
todo_list.add_url_rule(
        rule='/todos/<int:todo_id>',
        view_func=todos_view,
        methods=['GET', 'PATCH', 'PUT', 'DELETE'])
