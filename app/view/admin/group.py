from flask import request, url_for, redirect, render_template
from flask_login import login_required
from app.form.admin.group import GroupForm
from app.function.navigation import get_navigation_info
from app.function.permissions import permission_required
from app.model.auth import GroupAuthority
from app.model.group import UserGroup
from app.view.admin import admin


@admin.route('/group/')
@login_required
@permission_required("auth_admin_group")
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
@permission_required("auth_admin_add_group")
def add_group():
    navigation = get_navigation_info(title="用户组", sub_title="新的用户组", tag="add_group")
    GroupForm.init_auths_radio()
    form = GroupForm()
    if request.method == 'POST':
        auths = GroupAuthority.result_to_str(form)
        group = UserGroup(name=form.name.data, status=form.status.data, authority=auths)
        group.add_one()
        return redirect(url_for('admin.group'))
    if request.method == 'GET':
        return render_template('admin/edit_group.html', navigation=navigation, form=form)


@admin.route('/alter_group/<int:group_id>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_edit_group")
def alter_group(group_id):
    navigation = get_navigation_info(title="修改用户组", sub_title="修改已存在的用户组", tag="alter_group")
    GroupForm.init_auths_radio(group_id)
    form = GroupForm()
    if request.method == 'GET':
        group = UserGroup.query.filter_by(id=group_id).first()
        form.init_form(group.name, group.status)
        return render_template('admin/edit_group.html', navigation=navigation, form=form)
    if request.method == 'POST':
        auths = GroupAuthority.result_to_str(form)
        group = UserGroup.query.filter_by(id=group_id).first()
        group.update_group(name=form.name.data, status=form.status.data, authority=auths)
        return redirect(url_for('admin.group'))
