from flask import Blueprint

admin = Blueprint("admin", __name__)

from . import auth, cat, comment, error, group, index, login, moment, post, setting, test, user
