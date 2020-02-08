import os

from flask import request, make_response
from flask_login import current_user

from app import db
from app.model.user import UserAvatar
from app.view.tool import tool


@tool.route('/load_avatar/', methods=['GET', 'POST'])
def load_avatar():
    if request.method == "GET":
        avatar = db.session.query(UserAvatar.name, UserAvatar.path).filter(UserAvatar.uid == current_user.id,
                                                                           UserAvatar.name.startswith("b")).first()
        if avatar:
            src = os.path.join(avatar.path, avatar.name)
            image_data = open(src, 'rb').read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        return ""


@tool.route('/load_edit_avatar/<int:uid>', methods=['GET', 'POST'])
def load_edit_avatar(uid):
    if request.method == "GET":
        avatar = db.session.query(UserAvatar.name, UserAvatar.path).filter(UserAvatar.uid == uid,
                                                                           UserAvatar.name.startswith("b")).first()
        if avatar:
            src = os.path.join(avatar.path, avatar.name)
            image_data = open(src, 'rb').read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response