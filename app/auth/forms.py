# coding: utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'自动登陆')
    submit = SubmitField(u'登陆')


class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能包含a-Z字符, '
                                          u'数字, 点或者下划线')])
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField(u'设定密码', validators=[
        Required(), EqualTo('password2', message=u'输入的密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱地址已经被注册使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已经被注册使用')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'设定新密码', validators=[
        Required(), EqualTo('password2', message=u'输入的密码不匹配')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'提交')


class PasswordResetRequestForm(Form):
    email = StringField(u'注册邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'提交')


class PasswordResetForm(Form):
    email = StringField(u'注册邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'设定密码', validators=[
        Required(), EqualTo('password2', message=u'输入的密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱地址输入有误')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱地址已经被注册使用')
