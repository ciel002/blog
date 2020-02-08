from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email

from app import db
from app.model.group import UserGroup


class UserForm(FlaskForm):
    name = StringField('UserName', validators=[
        DataRequired(message="请输入用户名"),
        Length(message="长度最小6，最大24", min=6, max=24)
    ], render_kw={'class': 'form-control', 'placeholder': 'UserName'})
    password = PasswordField('Password', validators=[
        DataRequired(message="请输入密码"),
    ], render_kw={'class': 'form-control', 'placeholder': 'Password'})
    group_id = SelectField('Group', validators=[
        DataRequired(message="请选择用户组")
    ], render_kw={'class': 'form-control'}, coerce=int)
    ava = HiddenField('ava')
    phone = StringField('Phone', validators=[
        DataRequired(message="请输入手机号"),
        Length(message="长度最小11，最大24", min=11, max=15)
    ], render_kw={'class': 'form-control', 'placeholder': 'Phone'})
    email = StringField('Email', validators=[
        DataRequired(message="请输入Email"),
        Email("请输入正确的Email格式")
    ], render_kw={'class': 'form-control', 'placeholder': 'Email'})
    wechat = StringField('Wechat', validators=[
        DataRequired(message="请输入微信号")
    ], render_kw={'class': 'form-control', 'placeholder': 'Wechat'})
    signature = StringField('Signature', validators=[
        DataRequired(message="请输入个性签名"),
        Length(message="最大50个字符", min=0, max=50)
    ], render_kw={'class': 'form-control', 'placeholder': 'Signature'})
    submit = SubmitField('提交', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(UserForm, self).__init__()
        groups = db.session.query(UserGroup.id, UserGroup.name).all()
        self.group_id.choices = groups
        self.group_id.data = 4

    def alter_user(self, name, group, phone, email, wechat, signature):
        self.name.data = name
        self.group_id.data = group
        self.phone.data = phone
        self.email.data = email
        self.wechat.data = wechat
        self.signature.data = signature
