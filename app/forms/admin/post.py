from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.model.cat import Category
from app.model.group import UserGroup
from app.model.setting import Status, Property
from app.model.user import User


class PostForm(FlaskForm):
    title = StringField('PostTitle', validators=[DataRequired(message='请输入标题')]
                        , render_kw={'class': 'form-control', 'placeholder': 'Title'})
    abstract = TextAreaField('Abstract', validators=[DataRequired(message='请输入摘要')]
                             , render_kw={'class': 'form-control textarea-fixed', 'placeholder': 'Abstract'
            , 'style': 'height:200px;'})
    content = TextAreaField('Content', validators=[DataRequired(message='请输入内容')]
                            , render_kw={'class': 'form-control textarea-fixed', 'placeholder': 'Content'
            , 'style': 'height:400px;'})
    author = SelectField('Author', validators=[DataRequired(message='请选择作者')]
                         , render_kw={'class': 'form-control', 'placeholder': 'Author'})
    category_id = SelectField('Category', validators=[DataRequired(message='请选择分类')]
                              , render_kw={"class": "form-control"}
                              , coerce=int)
    rank = StringField('Rank', validators=[DataRequired(message='请输入文章排名')], render_kw={"class": "form-control"}
                       , default=0)
    is_top = SelectField('Rank', validators=[DataRequired(message='请输入文章是否置顶')]
                         , choices=[(0, '不置顶'), (1, '置顶')], render_kw={"class": "form-control"}, coerce=int)
    post_property = SelectField('Property', validators=[DataRequired(message='请选择属性')]
                                , render_kw={"class": "form-control"}, coerce=int)
    status = SelectField('Status', validators=[DataRequired(message='请选择状态')]
                         , render_kw={"class": "form-control"}, coerce=int)
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-primary'})

    def __init__(self):
        super(PostForm, self).__init__()
        # 获取作者列表, 过滤条件为 add_post 权限为 1 的用户, 获取的数据列表填充 author 下拉列表内容
        # groups = db.session.query(UserGroup.id).filter(UserGroup.authority.contains('2'))
        users = db.session.query(User.id, User.name).filter(User.group_id == UserGroup.id,
                                                            UserGroup.authority.contains('2')).all()
        # 获取分类列表
        categories = db.session.query(Category.id, Category.name).all()
        # 获取属性列表
        properties = db.session.query(Property.id, Property.name).all()
        # 获取状态列表
        status_list = db.session.query(Status.id, Status.name).filter(Status.id<=3).all()
        self.author.choices = users
        self.category_id.choices = categories
        self.post_property.choices = properties
        self.status.choices = status_list

    def alter_post(self, title, abstract, content, author, category_id, rank, is_top, post_property,
                   status):
        self.title.data = title
        self.abstract.data = abstract
        self.content.data = content
        self.author.data = author
        self.category_id.data = category_id
        self.rank.data = rank
        self.is_top.data = is_top
        self.post_property.data = post_property
        self.status.data = status
