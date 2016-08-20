# coding: utf-8
"""
app defined here
"""


from flask import Flask
from flask import request, session, make_response, redirect, abort, url_for, flash
from flask import render_template
from flask.ext.script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

#from models import Role, User
from local_settings import MySQL_URI, SECRET_KEY

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = MySQL_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = SECRET_KEY

manager = Manager(app)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app) # 插件

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html')


@app.route('/user/', methods=['GET','POST'])
def user_index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('user_detail'))
    return render_template('user_index.html',name=name,form=form)

@app.route('/user/<name>')
def user_detail(name=None):
    return render_template('user.html', name=name)
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #def make_shell_context():
    #    return dict(app=app,db=db,User=User,Role=Role)
    #manager.add_command("shell",Shell(make_context=make_shell_context))
    manager.run()
