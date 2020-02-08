import time

from sqlalchemy import func

from app import db
from app.common.constant import TABLE_PREFIX, STATUS_USEFUL, STATUS_PUBLISH



class Category(db.Model):
    __tablename__ = TABLE_PREFIX + 'categories'
    id = db.Column(db.Integer, primary_key=True)  # 分类ID
    pid = db.Column(db.Integer)  # 分类父ID
    name = db.Column(db.String(20), nullable=False)  # 分类名
    sub_name = db.Column(db.String(50), nullable=False)  # 分类副名称
    create_time = db.Column(db.DateTime)  # 分类创建时间
    update_time = db.Column(db.DateTime)  # 分类修改时间
    status = db.Column(db.Integer)  # 分类当前状态
    sort = db.Column(db.Integer)  # 分类排序数
    description = db.Column(db.String(100))  # 分类描述

    def __init__(self, name=None, sub_name=None, status=None, sort=None, description=None):
        self.name = name
        self.sub_name = sub_name
        self.status = status
        self.sort = sort
        self.description = description
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Category %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_category(self, name, sub_name, status, sort, description, pid=0):
        self.pid = pid
        self.name = name
        self.sub_name = sub_name
        self.status = status
        self.sort = sort
        self.description = description
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.session.commit()

    @staticmethod
    def get_categories_info(status=STATUS_USEFUL):
        from app.model.setting import Status
        return db.session.query(Category.id, Category.name, Category.sub_name, Category.sort,
                                Status.name.label("status"),
                                Category.create_time, Category.update_time, Category.description).filter(
            Category.status == Status.id, Status.id == status).all()

    @staticmethod
    def get_all_categories():
        from app.model.post import Post
        return db.session.query(Category.name, Category.sub_name
                                , func.count(Post.category_id).label('count')).filter(
            Post.status == STATUS_PUBLISH).outerjoin(Post,
                                                     Category.id == Post.category_id).group_by(
            Category.id).all()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()
