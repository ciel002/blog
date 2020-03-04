from flask import Blueprint

home: Blueprint = Blueprint("home", __name__)

from . import category, csgo, error, index, login, post, search, user