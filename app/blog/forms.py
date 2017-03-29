# coding: utf-8

from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    body = PageDownField(u"在这里写下你的文字(MarkDown语法)", validators=[Required()])
    submit = SubmitField(u'提交')
