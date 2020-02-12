import time

from sqlalchemy import func

from app import db
from app.common.constant import TABLE_PREFIX, DELETABLE_YES


class UserGroup(db.Model):
    __tablename__ = TABLE_PREFIX + 'users_groups'
    id = db.Column(db.Integer, primary_key=True)  # 用户组ID
    name = db.Column(db.String(30), nullable=False)  # 用户组名称
    create_time = db.Column(db.DateTime)  # 用户组创建时间
    update_time = db.Column(db.DateTime)  # 用户组更新时间
    status = db.Column(db.Integer)  # 用户组当前状态
    authority = db.Column(db.String(100))  # 用户组所拥有的权限
    deletable = db.Column(db.Integer, nullable=False)  # 是否可以删除

    def __init__(self, name, status, authority="", deletable=DELETABLE_YES):
        super(UserGroup, self).__init__()
        self.name = name
        self.deletable = deletable
        self.authority = authority
        self.status = status
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<UserGroup %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_group(self, name, status, authority):
        self.name = name
        self.status = status
        self.authority = authority
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.session.commit()

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()

    @staticmethod
    def get_groups_total():
        return db.session.query(func.count(UserGroup.id)).scalar()

    @staticmethod
    def get_groups_name():
        return db.session.query(UserGroup.id, UserGroup.name).all()
