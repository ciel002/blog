from flask import request, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.common.constant import STATUS_PUBLISH, STATUS_DELETED
from app.form.admin.moment import MomentForm
from app.function.config import get_config
from app.function.navigation import get_navigation_info
from app.function.paginate import get_admin_moments_paginate
from app.function.permissions import permission_required
from app.model.moment import Moment
from app.view.admin import admin


@admin.route('/moment/', methods=['GET', 'POST'])
@admin.route('/moment/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_post")
def moment(page=1):
    """
    动态列表页面
    :return:
    """
    navigation = get_navigation_info(title="动态列表", sub_title="所有动态", tag="moment")
    if request.method == 'GET':
        pagination = get_admin_moments_paginate(page, per_page=int(get_config("web_admin_post_per_page")))
        if request.args.get('moment_id') is not None:
            moment = Moment.query.filter_by(id=request.args.get('moment_id')).first()
            moment.update_status(status=STATUS_DELETED)
            return redirect(url_for('admin.post'))
        return render_template("admin/moment.html", navigation=navigation, moments=pagination.items,
                               pagination=pagination,
                               moments_total=len(pagination.items))


@admin.route('/add_moment/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_add_post")
def add_moment():
    """
    发布动态页面
    :return:
    """
    navigation = get_navigation_info(title="发布动态", sub_title="写一篇新的动态", tag="add_moment")
    form = MomentForm()
    if request.method == 'GET':
        return render_template("admin/edit_moment.html", navigation=navigation, form=form)
    if request.method == 'POST':
        moment = Moment(
            content=form.content.data,
            uid=current_user.id,
            moment_property=form.moment_property.data,
            status=form.status.data)
        moment.add_one()
        return redirect(url_for('admin.moment'))


@admin.route('/alter_moment/<int:moment_id>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_edit_post")
def alter_moment(moment_id):
    """
    修改动态页面
    通过文章页面传递过来的moment ID和TITLE  查询相应的动态，并将动态的内容显示在页面中供用户修改
    :param moment_id:
    :param moment_title:
    :return:
    """
    navigation = get_navigation_info(title="修改动态", sub_title="修改已发布的动态", tag="alter_moment")
    form = MomentForm()
    if request.method == 'GET':
        moment = Moment.query.filter_by(id=moment_id).first()
        form.alter_post(moment.content, moment.moment_property, moment.status)
        return render_template("admin/edit_moment.html", navigation=navigation, form=form)
    if request.method == 'POST':
        """
        method为POST
        通过传递的moment ID 查询相应的动态  更新动态内容
        """
        moment = Moment.query.filter_by(id=moment_id).first()
        moment.update_moment(content=form.content.data, status=form.status.data,
                             moment_property=form.moment_property.data)
        if form.status.data == STATUS_PUBLISH:
            return redirect(url_for('admin.moment'))
        elif form.status.data == STATUS_DELETED:
            return redirect(url_for('admin.dustbin_moment'))


@admin.route('/dustbin_moment/', methods=['GET', 'POST'])
@admin.route('/dustbin_moment/list/<int:page>', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_delete_post")
def dustbin_moment(page=1):
    """
    动态垃圾箱页面
    在此页面删除的动态将会在数据库中真正的删除，无法找回
    :return:
    """
    navigation = get_navigation_info(title="动态垃圾箱", sub_title="被删除的动态", tag="dustbin_moment")
    if request.method == 'GET':
        pagination = get_admin_moments_paginate(page, per_page=int(get_config("web_admin_post_per_page")),
                                              status=STATUS_DELETED)
        if request.args.get('moment_id') is not None:
            moment = Moment.query.filter_by(id=request.args.get('moment_id')).first()
            moment.real_delete()
            return redirect(url_for('admin.dustbin_moment'))
        return render_template("admin/moment.html", navigation=navigation, moments=pagination.items, pagination=pagination,
                               moments_total=len(pagination.items))
