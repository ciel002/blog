from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.model.setting import Property, Status


class MomentForm(FlaskForm):
    content = TextAreaField('动态内容', validators=[DataRequired(message='请输入内容')]
                            , render_kw={'class': 'form-control textarea-fixed', 'placeholder': 'Content',
                                         'style': 'height:200px;'})
    moment_property = SelectField('属性', validators=[DataRequired(message='请选择属性')]
                                  , render_kw={"class": "form-control"}, coerce=int)
    status = SelectField('状态', validators=[DataRequired(message='请选择状态')]
                         , render_kw={"class": "form-control"}, coerce=int)
    submit = SubmitField('发布', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(MomentForm, self).__init__()
        # 获取属性列表
        properties = db.session.query(Property.id, Property.name).all()
        # 获取状态列表
        status_list = db.session.query(Status.id, Status.name).filter(Status.id.between(2, 3)).all()
        self.moment_property.choices = properties
        self.status.choices = status_list

    def alter_post(self, content, moment_property, status):
        self.content.data = content
        self.moment_property.data = moment_property
        self.status.data = status
