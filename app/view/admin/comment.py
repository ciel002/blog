from flask import render_template, request, redirect, url_for
from flask_login import login_required

from app.common.constant import STATUS_DELETED, STATUS_PUBLISH
from app.function.config import get_config
from app.function.navigation import get_navigation_info
from app.function.paginate import get_admin_comments_paginate, get_admin_post_replies_paginate
from app.function.permissions import permission_required
from app.model.post import PostComment, PostReply
from app.view.admin import admin


@admin.route('/comment/', methods=['GET', 'POST'])
@admin.route('/comment/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_comment")
def comment(page=1):
    navigation = get_navigation_info(title="评论列表", tag="comment")
    pagination = get_admin_comments_paginate(page, per_page=int(get_config("web_admin_comment_per_page")),
                                             status=STATUS_PUBLISH)
    if request.method == 'GET':
        delete_id = request.args.get("delete_id")
        if delete_id:
            comment = PostComment.query.filter_by(id=delete_id).first()
            comment.update_status(status=STATUS_DELETED)
            return redirect(url_for('admin.comment'))
        return render_template("admin/comment.html", navigation=navigation, comments=pagination.items,
                               pagination=pagination, comments_count=len(pagination.items))


@admin.route('/dustbin_comment/', methods=['GET', 'POST'])
@admin.route('/dustbin_comment/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_delete_comment")
def dustbin_comment(page=1):
    navigation = get_navigation_info(title="辣鸡评论列表", tag="dustbin_comment")
    pagination = get_admin_comments_paginate(page, per_page=int(get_config("web_admin_comment_per_page")),
                                             status=STATUS_DELETED)
    if request.method == 'GET':
        restore_id = request.args.get("restore_id")
        delete_id = request.args.get("delete_id")
        if delete_id:
            comment = PostComment.query.filter_by(id=delete_id).first()
            comment.real_delete()
            return redirect(url_for('admin.dustbin_comment'))
        if restore_id:
            comment = PostComment.query.filter_by(id=restore_id).first()
            comment.update_status(status=STATUS_PUBLISH)
            return redirect(url_for('admin.dustbin_comment'))
        return render_template("admin/comment.html", navigation=navigation, comments=pagination.items,
                               pagination=pagination, comments_count=len(pagination.items))


@admin.route('/post_reply/', methods=['GET', 'POST'])
@admin.route('/post_reply/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_comment_reply")
def post_reply(page=1):
    navigation = get_navigation_info(title="文章回复列表", tag="post_reply")
    pagination = get_admin_post_replies_paginate(page, per_page=int(get_config("web_admin_comment_reply_per_page")),
                                                 status=STATUS_PUBLISH)
    if request.method == 'GET':
        delete_id = request.args.get("delete_id")
        if delete_id:
            reply = PostReply.query.filter_by(id=delete_id).first()
            reply.update_status(status=STATUS_DELETED)
            return redirect(url_for('admin.post_reply'))
        return render_template("admin/post_reply.html", navigation=navigation, replies=pagination.items, pagination=pagination,
                               replies_count=len(pagination.items))


@admin.route('/dustbin_post_reply/', methods=['GET', 'POST'])
@admin.route('/dustbin_post_reply/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_delete_comment_reply")
def dustbin_post_reply(page=1):
    navigation = get_navigation_info(title="文章回复列表垃圾箱", tag="dustbin_post_reply")
    pagination = get_admin_post_replies_paginate(page, per_page=int(get_config("web_admin_comment_reply_per_page")),
                                                 status=STATUS_DELETED)
    if request.method == 'GET':
        restore_id = request.args.get("restore_id")
        delete_id = request.args.get("delete_id")
        if delete_id:
            reply = PostReply.query.filter_by(id=delete_id).first()
            reply.real_delete()
            return redirect(url_for('admin.dustbin_post_reply'))
        if restore_id:
            reply = PostReply.query.filter_by(id=restore_id).first()
            reply.update_status(status=STATUS_PUBLISH)
            return redirect(url_for('admin.dustbin_post_reply'))
        return render_template("admin/post_reply.html", navigation=navigation, replies=pagination.items,
                               pagination=pagination,
                               replies_count=len(pagination.items))
