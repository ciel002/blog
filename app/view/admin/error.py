from flask import render_template, redirect, url_for

from app.function.navigation import get_navigation_info
from . import admin

"""
    异常处理视图
"""


@admin.errorhandler(401)
def have_not_login(error):
    return redirect(url_for("admin.login"))


@admin.errorhandler(403)
def have_not_permission(error):
    navigation = get_navigation_info(title="无法访问", sub_title="权限不足，请联系管理员", tag="authority")
    return render_template('admin/403.html', navigation=navigation, error=error), 403

@admin.errorhandler(404)
def have_not_found(error):
    navigation = get_navigation_info(title="404 NOT FOUND", sub_title="服务器上没有这个页面", tag="not_found")
    return render_template('admin/404.html', navigation=navigation, error=error), 404
