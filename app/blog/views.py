# coding: utf-8

from flask import render_template, redirect, request, url_for, flash,\
        current_app, abort
from flask_login import login_required, current_user
from . import blog
from .forms import PostForm
from ..main.forms import CommentForm
from .. import db
from ..models import Permission, Post, Comment


@blog.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts,
                           pagination=pagination)


@blog.route('/<int:id>', methods=['GET', 'POST'])
def post_page(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    # 于post发表评论
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'评论已发表')
        return redirect(url_for('blog.post_page', id=post.id, page=-1))
    # 渲染指定id的post,及其附带的评论(分页形式)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,
        per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template(
        'blog/post.html',
        form=form,
        posts=[post],
        comments=comments,
        pagination=pagination
    )


@blog.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash(u'文章已更新')
        return redirect(url_for('blog.post_page', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


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
