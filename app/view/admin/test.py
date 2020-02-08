from flask_wtf import FlaskForm
from wtforms import StringField

from app import db
from app.forms.admin.setting import SettingForm
from app.model.setting import Config
from app.view.admin import admin


@admin.route("/test/")
def test():
    config = db.session.query(Config.id, Config.name, Config.sub_name).filter(
        Config.sub_name.startswith("web_admin")).all()

    for item in config:
        setattr(SettingForm, item[2], StringField(item[1],
                                                  render_kw={"class": "form-control", 'placeholder': item[1]}))
    form = SettingForm()
    print(form)
    for item in form:
        print(item)
    # return render_template('index.html', form=form)
    return "123123"
