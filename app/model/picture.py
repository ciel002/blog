import time

from app import db
from app.common.constant import TABLE_PREFIX


class Picture(db.Model):
    __tablename__ = TABLE_PREFIX + 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    album_id = db.Column(db.Integer)
    description = db.Column(db.String(200))
    create_time = db.Column(db.DateTime)
    upload_time = db.Column(db.DateTime)

    def __init__(self, name, filename, md5, album_id, description=None):
        self.name = name
        self.filename = filename
        self.md5 = md5
        self.album_id = album_id
        self.description = description
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Picture %r>' % self.name

    def add_one(self):
        db.session.add(self)
        db.session.commit()
