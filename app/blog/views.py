# coding: utf-8

from flask import render_template, redirect, request, url_for, flash,\
        current_app, make_response
from flask_login import login_required, current_user
from . import blog
from .forms import PostForm
from .. import db
from ..models import Permission, Post


@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts,
                           show_followed=show_followed, pagination=pagination)


@blog.route('/show_all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('blog.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@blog.route('/show_followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('blog.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@blog.route('/writing', methods=['GET', 'POST'])
@login_required
def writing():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        flash(u'已完成发帖')
        return redirect(url_for('blog.index'))
    return render_template('blog/writing.html', form=form)
