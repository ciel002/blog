from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PropertyForm(FlaskForm):
    name = StringField('PropertyName', validators=[DataRequired(message='请输入属性名')]
                       , render_kw={"class": "form-control", 'placeholder': 'Name'})
    description = TextAreaField('Description', validators=[DataRequired(message='请输入描述信息')]
                                , render_kw={"class": "form-control textarea-fixed", 'placeholder': 'Description'})
    submit = SubmitField('Add', render_kw={'class': 'btn btn-primary'})