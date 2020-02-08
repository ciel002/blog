import os

from flask import redirect, url_for, request, render_template, json
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin.user import UserForm
from app.function.config import get_config
from app.function.img import md5_file, resize_avatar
from app.function.navigation import get_navigation_info
from app.function.paginate import get_admin_users_paginate
from app.function.permissions import admin_required
from app.model.group import UserGroup
from app.model.user import User
from app.view.admin import admin


@admin.route('/user/')
@admin.route('/user/list/<int:page>/')
@admin.route('/user/<string:gid>/')
@admin.route('/user/<string:gid>/list/<int:page>/')
@login_required
@admin_required
def user(gid=0, page=1):
    navigation = get_navigation_info(title="用户管理", sub_title="控制台", tag="user")
    pagination = get_admin_users_paginate(page, int(get_config("web_admin_user_per_page")), gid)
    groups = UserGroup.get_groups_name()
    if request.method == 'GET':
        if request.args.get('user_id') is not None:
            user = User.query.filter_by(id=request.args.get('user_id')).first()
            user.real_delete()
            return redirect(url_for('admin.user'))
        return render_template('admin/user.html', navigation=navigation, pagination=pagination,
                               users=pagination.items, users_total=len(pagination.items), groups=groups,
                               group_id=int(gid))


@admin.route('/add_user/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    navigation = get_navigation_info(title="添加用户", sub_title="新的用户", tag="add_user")
    form = UserForm()
    if request.method == 'GET':
        return render_template('admin/edit_user.html', navigation=navigation, form=form)
    if request.method == 'POST':
        user = User(name=form.username.data, password=form.password.data, group_id=form.group.data,
                    email=form.email.data, wechat=form.wechat.data, signature=form.signature.data)
        user.add_one()
        return redirect(url_for('admin.user'))


@admin.route('/alter_user/<int:user_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def alter_user(user_id):
    navigation = get_navigation_info(title="修改用户", sub_title="已存在的用户", tag="alter_user")
    form = UserForm()
    if request.method == 'GET':
        user = User.query.filter_by(id=user_id).first()
        form.alter_user(name=user.name, group=user.group_id, phone=user.phone, email=user.email,
                        wechat=user.wechat, signature=user.signature)
        return render_template('admin/edit_user.html', navigation=navigation, form=form, uid=user_id)
    if request.method == 'POST':
        user = User.query.filter_by(id=user_id).first()
        user.update_user(request.form)
        return redirect(url_for('admin.user'))


@admin.route('/alter_avatar/<int:uid>', methods=['GET', 'POST'])
def alter_avatar(uid):
    if request.method == 'POST':
        # 获取ajax传来的头像文件
        file = request.files.get("avatar")
        # 获取安全的文件名，用于保存
        name = secure_filename(file.filename)
        ext = os.path.splitext(name)[-1]
        import uuid
        filename = uuid.uuid4().hex + ext
        # 计算文件的MD5，防止重复保存
        md5 = md5_file(file)
        # 文件的保存路径
        path = get_config("web_system_upload_imgs_path")
        if not os.path.exists(path):
            os.mkdir(path)
        # 文件的保存路径
        file.save(os.path.join(path, filename))
        # 需要保存什么大小的头像
        sizes = {
            "s" + filename: 80,
            "m" + filename: 160,
            "b" + filename: 250
        }
        # 对头像进行裁剪和缩放
        avatar_id = resize_avatar(os.path.join(path, filename), path, uid, sizes)
        if avatar_id:
            # 删除之前在数据库中的头像
            return json.dumps({
                "error": 1,
                "msg": "成功",
            })
        return json.dumps({
            "error": 0,
            "msg": "失败",
        })
