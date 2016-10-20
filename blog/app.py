# coding: utf-8
"""
app defined here
"""
from functools import wraps
from flask import Flask
from flask import request, session, make_response, redirect, abort, url_for, flash
from flask import render_template
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


#from models import Role, User
from local_settings import MySQL_URI, SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = MySQL_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = SECRET_KEY

manager = Manager(app)
db = SQLAlchemy(app)

# represent style
bootstrap = Bootstrap(app)


def ops_record_broken(module_name='camel'):
    def deco(func):
        print 'deco'
        print module_name
        print func.__name__
        # print request.values
        # print request.url

        def warpped(*argu, **argv):
            return func(*argu, **argv)
        return warpped
    return deco


def ops_record(module_name='camel'):
    """closure return a deco"""
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs) 
            if request.environ['REQUEST_METHOD'] == 'GET':
                return resp
            print ':module_name:', module_name
            print ':func.__name__:', func.__name__
            print ':requ_env:', request.environ
            print ':requ.values:', request.values
            print ':form2dict:', request.form.to_dict()
            return resp
        return wrapper
    return deco


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    print ':user_agent:', user_agent
    return render_template('index.html')


@app.route('/user/', methods=['GET', 'POST', 'PUT'])
# @app.route('/user/<name>')
# @ops_record('user_part')
@ops_record('user')
def user_index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user_index'))
    return render_template('user_index.html', name=session.get('name', 'Not in session'), form=form)

#@app.route('/user/<name>')
# def user_profile(name='visitor'):
# return render_template('user.html', name=session.get('name','Not in
# session'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # def make_shell_context():
    #    return dict(app=app,db=db,User=User,Role=Role)
    # manager.add_command("shell",Shell(make_context=make_shell_context))
    manager.run()
