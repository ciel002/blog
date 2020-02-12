from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app.common.constant import STATUS_USEFUL, STATUS_USELESS
from app.function.navigation import get_navigation_info
from app.model.auth import GroupAuthority
from app.view.admin import admin
from app.function.permissions import permission_required


@admin.route('/auth/')
@login_required
@permission_required("auth_admin_auth")
def auth():
    navigation = get_navigation_info(title="权限列表", tag="auth")
    auths = GroupAuthority.get_all_auths(status=STATUS_USEFUL)
    if request.method == 'GET':
        delete_id = request.args.get("delete_id")
        if delete_id:
            auth = GroupAuthority.query.filter_by(id=delete_id).first()
            auth.update_status(status=STATUS_USELESS)
            return  redirect(url_for('admin.auth'))
        return render_template('admin/auth.html', navigation=navigation, auths=auths)


@admin.route('/add_auth/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_add_auth")
def add_auth():
    return


@admin.route('/alter_auth/<int:auth_id>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_edit_auth")
def alter_auth(auth_id):
    pass


@admin.route('/dustbin_auth/')
@login_required
@permission_required("auth_admin_delete_auth")
def dustbin_auth():
    navigation = get_navigation_info(title="弃用权限列表", tag="dustbin_auth")
    auths = GroupAuthority.get_all_auths(status=STATUS_USELESS)
    if request.method == 'GET':
        restore_id = request.args.get("restore_id")
        delete_id = request.args.get("delete_id")
        if restore_id:
            auth = GroupAuthority.query.filter_by(id=restore_id).first()
            auth.update_status(status=STATUS_USEFUL)
            return redirect(url_for('admin.dustbin_auth'))
        if delete_id:
            auth = GroupAuthority.query.filter_by(id=delete_id).first()
            auth.real_delete()
            return redirect(url_for('admin.dustbin_auth'))
        return render_template('admin/auth.html', navigation=navigation, auths=auths)
