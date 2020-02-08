import os
from manager import app
from app import db


@app.template_global("get_config")
def get_config(sub_name):
    from app.model.setting import Config
    value = db.session.query(Config.value).filter(Config.sub_name == sub_name).first()
    return value[0]
