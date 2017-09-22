"""wait to mv to topics dir"""
# coding: utf-8

from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required


class TweetForm(Form):
    body = TextAreaField(u"Wanna share some point to your follwer?", validators=[Required()])
    submit = SubmitField(u'tweet!')
