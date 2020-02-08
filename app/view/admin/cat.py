from flask import request, redirect, url_for, render_template
from flask_login import login_required

from app.common.constant import STATUS_USELESS
from app.forms.admin.cat import CategoryForm
from app.function.navigation import get_navigation_info
from app.function.permissions import admin_required
from app.model.cat import Category
from app.view.admin import admin


@admin.route('/category/', methods=['GET', 'POST'])
@login_required
@admin_required
def category():
    navigation = get_navigation_info(title="类别", tag="category")
    if request.method == 'GET':
        if request.args.get('category_id') is not None:
            category = Category.query.filter_by(id=request.args.get('category_id')).first()
            category.real_delete()
            return redirect(url_for('admin.category'))
        categories = Category.get_categories_info()
        return render_template('admin/category.html', navigation=navigation, categories=categories)


@admin.route('/add_category/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    navigation = get_navigation_info(title="添加类别", tag="add_category")
    form = CategoryForm()
    if request.method == 'GET':
        return render_template('admin/edit_category.html', navigation=navigation, form=form)
    if request.method == 'POST':
        category = Category(
            name=form.name.data,
            sub_name=form.sub_name.data,
            sort=form.sort.data,
            status=form.status.data,
            description=form.description.data)
        category.add_one()
        return redirect(url_for('admin.category'))


@admin.route('/alter_category/<int:category_id>/<category_sub_name>/', methods=['GET', 'POST'])
@login_required
@admin_required
def alter_category(category_id, category_sub_name):
    navigation = get_navigation_info(title="修改类别", tag="alter_category")
    form = CategoryForm()
    if request.method == 'GET':
        category = Category.query.filter_by(id=category_id).first()
        form.alter_category(
            name=category.name,
            sub_name=category.sub_name,
            sort=category.sort,
            status=category.status,
            description=category.description
        )
        return render_template('admin/edit_category.html', navigation=navigation, form=form)
    if request.method == 'POST':
        category = Category.query.filter_by(id=category_id).first()
        category.update_category(
            name=form.name.data,
            sub_name=form.sub_name.data,
            sort=form.sort.data,
            status=form.status.data,
            description=form.description.data
        )
        return redirect(url_for('admin.category'))


@admin.route('/dustbin_category/', methods=['GET', 'POST'])
@login_required
@admin_required
def dustbin_category():
    navigation = get_navigation_info(title="垃圾箱", tag="dustbin_category")
    if request.method == 'GET':
        if request.args.get('category_id') is not None:
            category = Category.query.filter_by(id=request.args.get('category_id')).first()
            category.real_delete()
            return redirect(url_for('admin.dustbin_category'))
        categories = Category.get_categories_info(STATUS_USELESS)
        return render_template('admin/dustbin_category.html', navigation=navigation, categories=categories)