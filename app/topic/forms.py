# coding: utf-8

from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required, Length
from ..main.forms import CommentForm


class TopicForm(Form):
    body = TextAreaField(
                    u"Wanna share some point to your follwer?",
                    validators=[Required(), Length(1, 160)]
    )
    submit = SubmitField(u'推！')
