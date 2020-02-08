import time

from app import db
from app.common.constant import TABLE_PREFIX, DELETABLE_YES


class Property(db.Model):
    __tablename__ = TABLE_PREFIX + 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime)
    deletable = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    def __init__(self, name=None, deletable=DELETABLE_YES, description=None):
        super(Property, self).__init__()
        self.name = name
        self.deletable = deletable
        self.description = description
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Property %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()


class Status(db.Model):
    __tablename__ = TABLE_PREFIX + 'status'
    id = db.Column(db.Integer, primary_key=True)  # 状态ID
    name = db.Column(db.String(20), nullable=False)  # 状态名
    create_time = db.Column(db.DateTime)  # 状态时间
    deletable = db.Column(db.Integer, nullable=False)  # 状态是否能够被删除
    description = db.Column(db.String(200))  # 状态描述

    def __init__(self, name=None, deletable=DELETABLE_YES, description=None):
        super(Status, self).__init__()
        self.name = name
        self.deletable = deletable
        self.description = description
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Status %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()


class Config(db.Model):
    __tablename__ = TABLE_PREFIX + "config"
    id = db.Column(db.Integer, primary_key=True)  # 配置项ID
    name = db.Column(db.String(30), nullable=False, unique=True)  # 配置名，用于显示
    sub_name = db.Column(db.String(50), nullable=False, unique=True)  # 配置子名，用于引用
    value = db.Column(db.Text)  # 配置内容
    remark = db.Column(db.String(100))  # 配置项描述
    sort = db.Column(db.Integer, default=0)  # 配置项排序
    status = db.Column(db.Integer, default=4)  # 配置项状态

    def __init__(self, name, sub_name, value, remark, sort, status):
        super(Config, self).__init__()
        self.name = name
        self.sub_name = sub_name
        self.value = value
        self.remark = remark
        self.sort = sort
        self.status = status

    def __repr__(self):
        return '<Config %r>' % self.name

    @staticmethod
    def set_config(form):
        for key, value in form.items():
            print(key, value)
            config = Config.get_config_by_name(key)
            print(config)
            if config:
                config.value = value
        db.session.commit()
        return True

    @staticmethod
    def get_config_type(type):
        return db.session.query(Config.id, Config.name, Config.sub_name, Config.value).filter(
            Config.sub_name.startswith(type)).order_by(Config.sort.desc()).all()

    @staticmethod
    def get_config_by_name(sub_name):
        return Config.query.filter_by(sub_name=sub_name).first()

    @staticmethod
    def get_config():
        config = dict()
        for item in Config.query.all():
            config[item.sub_name] = item.value
        return config

    def real_delete(self):
        if self.deletable is not 0:
            db.session.delete(self)
            db.session.commit()
