from flask import render_template

from app.function.paginate import get_home_category_paginate
from app.model.cat import Category
from app.model.post import Post
from app.view.home import home


@home.route('/category/<string:category_sub_name>')
@home.route('/category/<string:category_sub_name>/list/<int:page>')
def category(category_sub_name, page=1):
    categories = Category.get_all_categories()
    pagination = get_home_category_paginate(page=page, per_page=3, category_sub_name=category_sub_name)
    latest_posts = Post.get_latest_posts(5)
    return render_template(
        'home/index.html',
        current_category=category_sub_name,
        categories=categories,
        posts=pagination.items,
        latest_posts=latest_posts,
        pagination=pagination,
    )
