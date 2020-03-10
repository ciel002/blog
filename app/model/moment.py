import time

from app import db
from app.common.constant import TABLE_PREFIX, STATUS_PUBLISH, PROPERTY_PRIVATE, PROPERTY_PUBLIC
from app.model.user import User


class Moment(db.Model):
    __tablename__ = TABLE_PREFIX + 'moment'
    id = db.Column(db.Integer, primary_key=True)  # 动态ID
    uid = db.Column(db.Integer, nullable=False)  # 动态发布者ID
    content = db.Column(db.Text, nullable=False)  # 动态内容
    status = db.Column(db.Integer)  # 动态状态
    create_time = db.Column(db.DateTime)  # 动态创建时间
    moment_property = db.Column(db.Integer, nullable=False, default=PROPERTY_PRIVATE)  # 动态属性

    def __init__(self, uid=None, content=None, status=STATUS_PUBLISH, moment_property=PROPERTY_PUBLIC):
        self.content = content
        self.uid = uid
        self.status = status
        self.moment_property = moment_property
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Moment %r>' % self.id

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_moment(self, content, status, moment_property):
        self.content = content
        self.status = status
        self.moment_property = moment_property
        db.session.commit()

    def update_status(self, status):
        self.status = status
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_moments(page, limit):
        return db.session.query(Moment.id, Moment.uid, Moment.content, User.name.label("username"), Moment.create_time, User.avatar).outerjoin(User, User.id==Moment.uid).filter(
            Moment.uid == User.id).order_by(Moment.create_time.desc()).slice((page - 1)*limit, page*limit).all()
        pass
