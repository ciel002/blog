from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from app import db
from app.model.setting import Status


class CategoryForm(FlaskForm):
    name = StringField('类别名称', validators=[DataRequired(message='请输入分类名')]
                       , render_kw={"class": "form-control", 'placeholder': '类别名称'})
    sub_name = StringField('类别子名称', validators=[DataRequired(message='请输入分类名')]
                           , render_kw={"class": "form-control", 'placeholder': '类别子名称'})

    sort = StringField('排序', validators=[DataRequired(message='请输入文章排名')], render_kw={"class": "form-control"}
                       , default=0)
    status = SelectField('状态', validators=[DataRequired(message='请选择状态')]
                         , render_kw={"class": "form-control"}, coerce=int)
    description = TextAreaField('类别描述', render_kw={"class": "form-control textarea-fixed", 'placeholder': '类别描述'})
    submit = SubmitField('新增', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(CategoryForm, self).__init__()
        status_list = db.session.query(Status.id, Status.name).filter(Status.id.between(4,6)).all()
        self.status.choices = status_list

    def alter_category(self, name, sub_name, sort, status, description):
        self.name.data = name
        self.sub_name.data = sub_name
        self.sort.data = sort
        self.status.data = status
        self.description.data = description
