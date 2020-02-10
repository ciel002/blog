from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    Email = StringField('邮箱', validators=[
        DataRequired(message='请输入用户名'),
        Email("请输入正确的邮箱格式")
    ], render_kw={"class": "form-control", 'placeholder': 'Email'})
    Password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码')
    ], render_kw={"class": "form-control", 'placeholder': 'Password'})
    VerifyCode = StringField('验证码', validators=[DataRequired('请输入验证码')],
                                   render_kw={"class": "form-control", 'placeholder': 'VerifyCode'})
    submit = SubmitField('登录', render_kw={'class': 'btn btn-primary'})