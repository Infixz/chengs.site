# coding: utf-8
"""
app defined here
"""
from __future__ import absolute_import
from functools import wraps

from flask import Flask
from flask import request, session
from flask import render_template, make_response, \
        redirect, abort, url_for, flash, jsonify
from flask.views import MethodView
from flask.ext.mail import Mail, Message
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

from wtforms import StringField, SubmitField
from wtforms.validators import Required

from local_settings import MySQL_URI, SECRET_KEY,\
        MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# mail init
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
mail = Mail(app)

# db init
app.config['SQLALCHEMY_DATABASE_URI'] = MySQL_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

# Manager & shell context
manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

# migrate
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# represent style
Bootstrap(app)


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

# Model


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html')


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
                'user_list': [
                    {'user_id': item.id, 'name': item.username} for item in User.query.all()],
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
            msg = Message(
                    'Add user',
                    sender='infixz@foxmail.com',
                    recipients=['sorrible@126.com'])
            msg.html = '<h3>Username: %s, role: %s</h3>' % (username, role_name)
            with app.app_context():
                mail.send(msg)
            return jsonify({'status': 'create sucessful'}), 201
        else:
            return jsonify({'status': 'check your args'}), 400

    def put(self, user_name):
        return jsonify({'status': 'un Authed'})

    def delete(self, user_name):
        return jsonify({'status': 'un Authed'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

user_view = UserAPI.as_view('user_api')

app.add_url_rule(
        rule='/users/',
        defaults={'user_name': None},
        view_func=user_view,
        methods=['GET', ])
app.add_url_rule(
        rule='/users/',
        view_func=user_view,
        methods=['POST', ])
app.add_url_rule(
        rule='/users/<user_name>',
        view_func=user_view,
        methods=['GET', 'PUT', 'DELETE'])


def make_shell_context():
    return dict(app=app, mail=mail, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
    """app.run(
        debug=True,
        host="0.0.0.0",
        port=8080)"""
