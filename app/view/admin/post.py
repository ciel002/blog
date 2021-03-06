from flask import url_for, redirect, request, render_template
from flask_login import login_required, current_user

from app.common.constant import STATUS_PUBLISH, STATUS_DRAFT, STATUS_DELETED
from app.form.admin.post import PostForm
from app.function.config import get_config
from app.function.navigation import get_navigation_info
from app.function.paginate import get_admin_posts_paginate
from app.function.permissions import permission_required
from app.model.post import Post
from app.view.admin import admin


@admin.route('/post/', methods=['GET', 'POST'])
@admin.route('/post/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_post")
def post(page=1):
    """
    文章页面
    :return:
    """
    navigation = get_navigation_info(title="文章", sub_title="所有文章", tag="post")
    if request.method == 'GET':
        pagination = get_admin_posts_paginate(page, per_page=int(get_config("web_admin_post_per_page")))
        if request.args.get('post_id') is not None:
            post = Post.query.filter_by(id=request.args.get('post_id')).first()
            post.delete()
            return redirect(url_for('admin.post'))
        return render_template("admin/post.html", navigation=navigation, posts=pagination.items, pagination=pagination,
                               posts_total=len(pagination.items))


@admin.route('/add_post/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_add_post")
def add_post():
    """
    写文章页面
    :return:
    """
    navigation = get_navigation_info(title="写文章", sub_title="写一篇新的文章", tag="add_post")
    form = PostForm()
    if request.method == 'GET':
        return render_template("admin/edit_post.html", navigation=navigation, form=form)
    if request.method == 'POST':
        post = Post(
            title=form.title.data,
            abstract=form.abstract.data,
            content=form.content.data,
            uid=current_user.id,
            category_id=form.category_id.data,
            rank=form.rank.data,
            is_top=form.is_top.data,
            post_property=form.post_property.data,
            status=form.status.data)
        post.add_one()
        return redirect(url_for('admin.post'))


@admin.route('/alter_post/<int:post_id>/<post_title>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_edit_post")
def alter_post(post_id, post_title):
    """
    修改文章页面
    通过  文章页面传递过来的post ID和TITLE  查询相应的文章，并将文章的内容显示在页面中供用户修改
    :param post_id:
    :param post_title:
    :return:
    """
    navigation = get_navigation_info(title="修改文章", sub_title="修改已发布的文章", tag="alter_post")
    form = PostForm()
    if request.method == 'GET':
        post = Post.query.filter_by(id=post_id).first()
        form.alter_post(post.title, post.abstract, post.content, post.category_id
                        , post.rank, post.is_top, post.post_property, post.status)
        return render_template("admin/edit_post.html", navigation=navigation, form=form)
    if request.method == 'POST':
        """
        method为POST
        通过传递的post ID 查询相应的post  更新post内容
        """
        post = Post.query.filter_by(id=post_id).first()
        post.update_post(form.title.data, form.abstract.data, current_user.id, form.content.data,
                         form.category_id.data, form.rank.data, form.is_top.data,
                         form.post_property.data, form.status.data)
        if form.status.data == STATUS_DRAFT:
            return redirect(url_for('admin.draft_post'))
        elif form.status.data == STATUS_PUBLISH:
            return redirect(url_for('admin.post'))
        elif form.status.data == STATUS_DELETED:
            return redirect(url_for('admin.dustbin_post'))


@admin.route('/draft_post/', methods=['GET', 'POST'])
@admin.route('/draft_post/list/<int:page>/', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_draft_post")
def draft_post(page=1):
    """
    草稿箱页面
    :return:
    """
    navigation = get_navigation_info(title="草稿箱", sub_title="修改未发布的文章", tag="draft_post")
    if request.method == 'GET':
        pagination = get_admin_posts_paginate(page, per_page=int(get_config("web_admin_post_per_page")), status=STATUS_DRAFT)
        if request.args.get('post_id') is not None:
            post = Post.query.filter_by(id=request.args.get('post_id')).first()
            post.delete()
            return redirect(url_for('admin.post'))
        return render_template("admin/post.html", navigation=navigation, posts=pagination.items, pagination=pagination,
                               posts_total=len(pagination.items))


@admin.route('/dustbin_post/', methods=['GET', 'POST'])
@admin.route('/dustbin_post/list/<int:page>', methods=['GET', 'POST'])
@login_required
@permission_required("auth_admin_delete_post")
def dustbin_post(page=1):
    """
    垃圾箱页面
    在此页面删除的文章将会在数据库中真正的删除，无法找回
    :return:
    """
    navigation = get_navigation_info(title="垃圾箱", sub_title="被删除的文章", tag="dustbin_post")
    if request.method == 'GET':
        pagination = get_admin_posts_paginate(page, per_page=int(get_config("web_admin_post_per_page")), status=STATUS_DELETED)
        if request.args.get('post_id') is not None:
            post = Post.query.filter_by(id=request.args.get('post_id')).first()
            post.real_delete()
            return redirect(url_for('admin.post'))
        return render_template("admin/post.html", navigation=navigation, posts=pagination.items, pagination=pagination,
                               posts_total=len(pagination.items))
