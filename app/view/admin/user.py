import os

from flask import redirect, url_for, request, render_template, json
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin.user import UserForm
from app.function.avatar import resize_avatar, alter_avatar
from app.function.config import get_config
from app.function.img import md5_file
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


@admin.route('/alter_user/<int:uid>/', methods=['GET', 'POST'])
@login_required
@admin_required
def alter_user(uid):
    navigation = get_navigation_info(title="修改用户", sub_title="已存在的用户", tag="alter_user")
    form = UserForm()
    if request.method == 'GET':
        user = User.query.filter_by(id=uid).first()
        form.alter_user(name=user.name, group=user.group_id, phone=user.phone, email=user.email,
                        wechat=user.wechat, signature=user.signature)
        return render_template('admin/edit_user.html', navigation=navigation, form=form, uid=uid)
    if request.method == 'POST':
        user = User.query.filter_by(id=uid).first()
        user.update_user(request.form)
        return redirect(url_for('admin.user'))


@admin.route('/alter_user_avatar/<int:uid>', methods=['GET', 'POST'])
def alter_user_avatar(uid):
    if request.method == 'GET':
        navigation = get_navigation_info(title="修改头像", tag="alter_user")
        return render_template('admin/edit_user_avatar.html', navigation=navigation, uid=uid)
    if request.method == 'POST':
        # 获取ajax传来的头像文件
        file = request.files.get("avatar")
        if alter_avatar(file, uid):
            return json.dumps({
                "error": 1,
                "msg": "成功",
            })
        return json.dumps({
            "error": 0,
            "msg": "失败",
        })
