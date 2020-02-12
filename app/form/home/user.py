from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from app.form.BaseForm import CustomForm


class ResetPasswordForm(CustomForm):
    Email = StringField('邮箱地址', render_kw={"class": "form-control", 'placeholder': '请输入该账号注册的邮箱地址', 'disabled': 'true'})
    Password = PasswordField('新密码', validators=[
        DataRequired(message='请输入密码')
    ], render_kw={"class": "form-control", 'placeholder': '请输入重置的密码'})
    SmsCode = StringField('邮箱验证码', validators=[DataRequired(message='请输入邮箱验证码'), Length(max=6, message="邮箱验证码错误")],
                          render_kw={"class": "form-control pull-left", 'placeholder': '请输入邮箱验证码'})
    submit = SubmitField('修改', render_kw={'class': 'btn btn-primary', 'onclick': 'return false;'})


class ResetEmailForm(CustomForm):
    OldEmail = StringField('邮箱地址', render_kw={"class": "form-control", 'disabled': 'true'})
    NewEmail = StringField('新邮箱地址', validators=[
        DataRequired(message='新邮箱地址'), Email("请输入正确的邮箱格式")
    ], render_kw={"class": "form-control", 'placeholder': '请输入重置的邮箱地址'})
    SmsCode = StringField('原邮箱验证码', validators=[DataRequired(message='请输入原邮箱验证码'), Length(max=6, message="邮箱验证码错误")],
                          render_kw={"class": "form-control pull-left", 'placeholder': '请输入原邮箱验证码'})
    submit = SubmitField('修改', render_kw={'class': 'btn btn-primary', 'onclick': 'return false;'})
