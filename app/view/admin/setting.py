from flask import redirect, url_for, request, render_template
from flask_login import current_user, login_required
from wtforms import StringField

from app.form.admin.property import PropertyForm
from app.form.admin.setting import SettingForm
from app.form.admin.status import StatusForm
from app.function.navigation import get_navigation_info
from app.function.permissions import permission_required
from app.model.setting import Status, Property, Config
from app.view.admin import admin


@admin.route('/status/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_status")
def status():
    navigation = get_navigation_info(title="状态", tag="status")
    form = StatusForm()
    if request.method == 'GET':
        if request.args.get('item_id') is not None:
            status = Status.query.filter_by(id=request.args.get('item_id')).first()
            status.real_delete_by_id()
            return redirect(url_for('admin.status'))
        status_list = Status.query.all()
        return render_template('admin/status.html', navigation=navigation, form=form, status_list=status_list)
    if request.method == 'POST':
        stat = Status(name=form.name.data, description=form.description.data)
        stat.add_one()
        return redirect(url_for('admin.status'))


@admin.route('/property/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_property")
def property():
    user = current_user
    navigation = get_navigation_info(title="属性", tag="property")
    form = PropertyForm()
    if request.method == 'GET':
        if request.args.get('item_id') is not None:
            property = Property.query.filter_by(id=request.args.get('item_id')).first()
            property.real_delete_by_id()
            return redirect(url_for('admin.property'))
        properties = Property.query.all()
        return render_template('admin/property.html', navigation=navigation, user=user, form=form, properties=properties)
    if request.method == 'POST':
        property = Property(name=form.name.data, description=form.description.data)
        property.add_one()
        return redirect(url_for('admin.property'))


@admin.route('/setting/<string:type>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_system_config")
def setting(type):
    if "home" in type:
        box_title = "主页设置"
        navigation = get_navigation_info(title="主页设置", tag="home")
    elif "admin" in type:
        box_title = "后台设置"
        navigation = get_navigation_info(title="后台设置", tag="admin")
    elif "mail" in type:
        box_title = "邮件设置"
        navigation = get_navigation_info(title="邮件设置", tag="mail")
    elif "system" in type:
        box_title = "系统设置"
        navigation = get_navigation_info(title="系统设置", tag="system")

    # 获取特定类型的配置项
    config = Config.get_config_type(type)
    # 获取所有类型的配置项
    all_config = Config.get_config()

    # 清空SettingForm表单中原有的配置项
    for item in all_config:
        if hasattr(SettingForm, item):
            delattr(SettingForm, item)

    # 添加新的配置项
    for item in config:
        setattr(SettingForm, item[2], StringField(item[1],
                                                  render_kw={"class": "form-control", 'placeholder': item[1]},
                                                  default=item[3]))
    form = SettingForm()
    if request.method == 'GET':
        return render_template('admin/setting.html', navigation=navigation, form=form, box_title=box_title)
    if request.method == 'POST':
        if Config.set_config(request.form.to_dict()):
            return redirect(request.url)
