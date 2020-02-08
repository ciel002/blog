from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from app import db
from app.model.setting import Status


class GroupForm(FlaskForm):
    name = StringField('GroupName', validators=[DataRequired(message='请输入用户组名')], render_kw={"class": "form-control"})
    status = SelectField('Status', validators=[DataRequired(message='请选择状态')]
                         , render_kw={"class": "form-control"}, coerce=int)
    submit = SubmitField('提交', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(GroupForm, self).__init__()
        status_list = db.session.query(Status.id, Status.name).filter(Status.id.between(4, 6)).all()
        self.status.choices = status_list
