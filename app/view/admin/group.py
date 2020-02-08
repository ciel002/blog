from flask import request, url_for, redirect, render_template
from flask_login import login_required

from app.forms.admin.group import GroupForm
from app.function.navigation import get_navigation_info
from app.function.permissions import admin_required
from app.model.group import UserGroup
from app.view.admin import admin


@admin.route('/group/')
@login_required
@admin_required
def group():
    navigation = get_navigation_info(title="用户组管理", sub_title="控制台", tag="group")
    groups = UserGroup.query.all()
    groups_total = UserGroup.get_groups_total()
    if request.method == 'GET':
        if request.args.get('group_id') is not None:
            group = UserGroup.query.filter_by(id=request.args.get('group_id')).first()
            group.real_delete()
            return redirect(url_for('admin.group'))
        return render_template('admin/group.html', navigation=navigation,
                               groups=groups, groups_total=groups_total)


@admin.route('/add_group/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_group():
    navigation = get_navigation_info(title="用户组", sub_title="新的用户组", tag="add_group")
    form = GroupForm()
    if request.method == 'POST':
        group = UserGroup(name=form.name.data, status=form.status.data)
        group.add_one()
        return redirect(url_for('admin.user'))
    if request.method == 'GET':
        return render_template('admin/edit_group.html', navigation=navigation, form=form)


@admin.route('/alter_group/<int:group_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def alter_group(group_id):
    navigation = get_navigation_info(title="修改用户组", sub_title="修改已存在的用户组", tag="alter_group")
    form = GroupForm()
    if request.method == 'GET':
        group = UserGroup.query.filter_by(id=group_id).first()
        form.alter_group(group.name)
        return render_template('admin/edit_group.html', navigation=navigation, form=form)
    if request.method == 'POST':
        group = UserGroup.query.filter_by(id=group_id).first()
        group.update_group(form.name.data, form.authority_add_post.data, form.authority_delete_post.data,
                           form.authority_comment_post.data, form.authority_visit_post.data)
        return redirect(url_for('admin.user'))
