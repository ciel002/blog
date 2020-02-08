from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms.BaseForm import CustomForm


class LoginForm(CustomForm):
    Email = StringField('Email', validators=[
        DataRequired(message='请输入用户名'),
        Email("请输入正确的邮箱格式")
    ], render_kw={"class": "form-control", 'placeholder': 'Email'})
    Password = PasswordField('Password', validators=[
        DataRequired(message='请输入密码')
    ], render_kw={"class": "form-control", 'placeholder': 'Password'})
    VerifyCode = StringField('VerifyCode', validators=[DataRequired('请输入验证码')],
                             render_kw={"class": "form-control", 'placeholder': 'VerifyCode'})
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary', 'onclick': 'return false;'})


class RegisterForm(CustomForm):
    Email = StringField('Email', validators=[
        DataRequired(message='请输入邮箱'),
        Email("请输入正确的邮箱格式")
    ], render_kw={"class": "form-control", 'placeholder': '电子邮箱为登录的账号名'})
    Name = StringField('Name', validators=[DataRequired(message='请输入用户昵称'),
                                           Length(min=6, max=18, message="昵称最短为2个汉字，最长为6个汉字")],
                       render_kw={"class": "form-control", 'placeholder': '请输入昵称'})
    Password = PasswordField('Password', validators=[
        DataRequired(message='请输入密码')
    ], render_kw={"class": "form-control", 'placeholder': '请输入密码'})
    RePassword = PasswordField('RePassword', validators=[
        DataRequired(message='请输入密码'), EqualTo(fieldname='Password', message='两次密码不一致')
    ], render_kw={"class": "form-control", 'placeholder': '请输入确认密码'})
    SmsCode = StringField('SmsCode', validators=[DataRequired(message='请输入邮箱验证码'), Length(max=6, message="邮箱验证码错误")],
                          render_kw={"class": "form-control", 'placeholder': '请输入邮箱验证码'})
    VerifyCode = StringField('VerifyCode', validators=[DataRequired('请输入验证码')],
                             render_kw={"class": "form-control", 'placeholder': 'VerifyCode'})
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary', 'onclick': 'return false;'})
