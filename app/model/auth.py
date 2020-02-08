import time

from app import db
from app.common.constant import DELETABLE_YES, TABLE_PREFIX


class GroupAuthority(db.Model):
    __tablename__ = TABLE_PREFIX + 'groups_authorities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 权限ID
    name = db.Column(db.String(30))  # 权限名
    deletable = db.Column(db.Integer, nullable=False)  # 是否能够被删除
    status = db.Column(db.Integer)  # 权限当前状态
    create_time = db.Column(db.DateTime)  # 权限创建时间
    update_time = db.Column(db.DateTime)  # 权限更新时间
    description = db.Column(db.String(100))  # 权限描述

    def __init__(self, name, description, deletable=DELETABLE_YES):
        super(GroupAuthority, self).__init__()
        self.name = name
        self.deletable = deletable
        self.description = description
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<UserAuthority %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_authority(self, name, description):
        self.name = name
        self.description = description
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.session.commit()

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()

    def update_status(self, status):
        self.status = status
        db.session.commit()

    @staticmethod
    def get_all_auths(status):
        return GroupAuthority.query.filter_by(status=status).all()
