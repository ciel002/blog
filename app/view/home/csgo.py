from flask import render_template

from app import db
from app.view.home import home


@home.route('/csgo/data')
def csgo_data():
    return render_template('home/csgo_data.html')


# @home.route('/csgo/data/5e')
# def csgo_data_5e():
#     return
