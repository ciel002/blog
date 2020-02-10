from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PropertyForm(FlaskForm):
    name = StringField('属性名称', validators=[DataRequired(message='请输入属性名')]
                       , render_kw={"class": "form-control", 'placeholder': 'Name'})
    description = TextAreaField('属性描述', validators=[DataRequired(message='请输入描述信息')]
                                , render_kw={"class": "form-control textarea-fixed", 'placeholder': 'Description'})
    submit = SubmitField('添加', render_kw={'class': 'btn btn-primary'})