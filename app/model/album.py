import time

from app import db
from app.common.constant import TABLE_PREFIX, PROPERTY_PRIVATE


class Album(db.Model):
    __tablename__ = TABLE_PREFIX + 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    album_property = db.Column(db.Integer, nullable=False, default=PROPERTY_PRIVATE)
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Album %r>' % self.name