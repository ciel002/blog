from wtforms import TextAreaField
from wtforms.validators import DataRequired

from app.forms.BaseForm import CustomForm


class CommentForm(CustomForm):
    content = TextAreaField('评论', validators=[DataRequired(message='评论不能为空')], render_kw={"class": "form-control"})

