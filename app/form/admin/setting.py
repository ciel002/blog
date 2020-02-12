from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField
from wtforms.form import BaseForm

# 动态生成表单内容，由视图完成
class SettingForm(FlaskForm):
    submit = SubmitField('保存', render_kw={'class': 'btn btn-primary'})
