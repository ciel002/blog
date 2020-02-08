from wtforms import StringField
from wtforms.validators import DataRequired

from app.forms.BaseForm import CustomForm


class CommentForm(CustomForm):
    content = StringField('GroupName', validators=[DataRequired(message='评论不能为空')], render_kw={"class": "form-control"})

