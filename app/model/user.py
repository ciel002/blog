import os
import time

from flask import request, current_app
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.model.group import UserGroup
from app.common.constant import DELETABLE_YES, GROUP_USER, TABLE_PREFIX
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    __tablename__ = TABLE_PREFIX + 'users'
    id = db.Column(db.Integer, primary_key=True)  # 用户ID
    name = db.Column(db.String(80), nullable=False, unique=True)  # 用户名
    password = db.Column(db.String(250), nullable=False)  # 用户密码
    group_id = db.Column(db.Integer, nullable=False)  # 用户组ID
    avatar = db.Column(db.Boolean, default=0)  # 用户是否有头像
    phone = db.Column(db.String(15))  # 用户手机号
    email = db.Column(db.String(50), unique=True)  # 用户EMAIL
    wechat = db.Column(db.String(100), unique=True)  # 用户微信号
    signature = db.Column(db.String(50))  # 个性签名
    register_time = db.Column(db.DateTime)  # 注册时间
    register_ip = db.Column(db.String(20))  # 注册IP地址
    login_times = db.Column(db.Integer, default=0)  # 用户登录次数
    last_login_ip = db.Column(db.String(20))  # 上次登录IP地址
    last_login_time = db.Column(db.DateTime)  # 上次登录时间
    update_time = db.Column(db.DateTime)  # 用户更新个人信息时间
    deletable = db.Column(db.Integer, nullable=False)  # 是否可以删除

    def __init__(self, name=None, password=None
                 , group_id=GROUP_USER, phone=None, email=None, wechat=None, signature=None, deletable=DELETABLE_YES):
        super(User, self).__init__()
        self.name = name
        self.set_hash_password(password)
        self.group_id = group_id
        self.phone = phone
        self.email = email
        self.wechat = wechat
        self.signature = signature
        self.deletable = deletable
        self.register_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.register_ip = request.remote_addr
        self.last_login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def set_hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_hash_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.name

    def add_one(self, avatar_id):
        db.session.add(self)
        db.session.commit()

    def update_user(self, data):
        for key, value in data.items():
            if hasattr(User, key) and value:
                setattr(self, key, value)
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.session.commit()

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()

    @staticmethod
    def get_users_count(gid):
        if int(gid) == 0:
            return db.session.query(func.count(User.id)).scalar()
        else:
            return db.session.query(func.count(User.id)).filter(UserGroup.id == gid).scalar()

    @staticmethod
    def get_users_info(gid):
        from app.model.post import Post, PostComment
        if int(gid) == 0:
            table4 = db.session.query(User.id, User.name, UserGroup.name.label('groupname')
                                      , User.register_time, User.last_login_time, User.email, User.wechat,
                                      User.deletable
                                      , func.count(PostComment.uid).label('comment_total'), User.deletable).outerjoin(
                PostComment,
                User.id == PostComment.uid).filter(
                UserGroup.id == User.group_id).group_by(User.id).subquery()

        else:
            table4 = db.session.query(User.id, User.name, UserGroup.name.label('groupname')
                                      , User.register_time, User.last_login_time, User.email, User.wechat,
                                      User.deletable
                                      , func.count(PostComment.uid).label('comment_total'), User.deletable).outerjoin(
                PostComment,
                User.id == PostComment.uid).filter(
                UserGroup.id == User.group_id, UserGroup.id == gid).group_by(User.id).subquery()

        results = db.session.query(table4.c.id, table4.c.name, table4.c.groupname, table4.c.register_time,
                                   table4.c.last_login_time, func.count(Post.uid).label('post_total'),
                                   table4.c.comment_total, table4.c.email, table4.c.wechat,
                                   table4.c.deletable).outerjoin(
            Post, Post.uid == table4.c.id).group_by(table4.c.id).all()

        return results

    def can(self, permission):
        authority = db.session.query(UserGroup.authority).filter(UserGroup.id == self.group_id).first()
        if str(permission) in authority[0]:
            return True
        return False

    def is_administrator(self):
        return self.can(1)

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode(encoding="utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        user = User.query.get(uid)
        user.set_hash_password(new_password)
        db.session.commit()
        return True


class UserActivated(db.Model):
    __tablename__ = TABLE_PREFIX + "users_activated"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # 验证类型为Email或者Phone
    name = db.Column(db.String(40))  # 验证邮箱或手机号
    validation = db.Column(db.Boolean, default=False)  # 是否验证，默认为False
    token = db.Column(db.String(50))  # 验证令牌
    create_time = db.Column(db.DateTime)  # 验证创建时间

    def __init__(self, name, type, token):
        super(UserActivated, self).__init__()
        self.name = name
        self.type = type
        self.token = token
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def update_validation(self):
        self.validation = True
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()


class UserAvatar(db.Model):
    __tablename__ = TABLE_PREFIX + "users_avatar"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)  # 头像所属用户ID
    name = db.Column(db.String(40))  # 头像名
    path = db.Column(db.String(200), default="")  # 头像存储路径
    # md5 = db.Column(db.String(128))  # 头像文件的MD5
    create_time = db.Column(db.DateTime)  # 验证创建时间

    def __init__(self, uid, name, path, ):
        super(UserAvatar, self).__init__()
        self.uid = uid
        self.name = name
        self.path = path
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def add_one(self):
        db.session.add(self)
        db.session.commit()
