# coding: utf-8

from __future__ import absolute_import
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from .local_settings import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(config[env_name])
    config[env_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .topic import topic as topic_blueprint
    app.register_blueprint(topic_blueprint, url_prefix='/topic')

    from .chatting import chatting as chatting_blueprint
    app.register_blueprint(chatting_blueprint, url_prefix='/chatting')

    from .todo_list import todo_list as todo_list_blueprint
    app.register_blueprint(todo_list_blueprint, url_prefix='/todo_list')

    """from .admin import admin as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/admin')"""

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
