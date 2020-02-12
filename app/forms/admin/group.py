from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from app import db
from app.common.constant import STATUS_USEFUL
from app.model.auth import GroupAuthority
from app.model.group import UserGroup
from app.model.setting import Status


class GroupForm(FlaskForm):
    name = StringField('用户组名称', validators=[DataRequired(message='请输入用户组名')], render_kw={"class": "form-control"})
    status = SelectField('状态', validators=[DataRequired(message='请选择状态')]
                         , render_kw={"class": "form-control"}, coerce=int)
    submit = SubmitField('提交', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(GroupForm, self).__init__()
        status_list = db.session.query(Status.id, Status.name).filter(Status.id.between(4, 6)).all()
        self.status.choices = status_list

    def init_form(self, name, stauts):
        self.name.data = name
        self.status.data = stauts

    @staticmethod
    def init_auths_radio(group_id=None):
        auths = GroupAuthority.get_all_auths(status=STATUS_USEFUL)
        group = UserGroup.query.filter_by(id=group_id).first()
        has_auths = group.authority.split(",") if hasattr(group, 'authority') else ""
        for auth in auths:
            setattr(GroupForm, auth.sub_name, RadioField(auth.name, validators=[DataRequired("请选择" + auth.name + "权限")],
                                                         render_kw={"class": "wtf-radio-box radio-inline"},
                                                         choices=[('0', '否'), (auth.id, '是')], coerce=int,
                                                         default=auth.id if str(auth.id) in has_auths else 0))
