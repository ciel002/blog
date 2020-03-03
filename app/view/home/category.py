from flask import render_template

from app.function.paginate import get_home_category_paginate
from app.function.redis import increase_explore_count
from app.model.post import Post
from app.view.home import home


@home.route('/category/<string:category_sub_name>')
@home.route('/category/<string:category_sub_name>/list/<int:page>')
@increase_explore_count
def category(category_sub_name, page=1):
    from app.function.config import get_config
    pagination = get_home_category_paginate(page=page, per_page=int(get_config("web_home_posts_pages")), category_sub_name=category_sub_name)
    latest_posts = Post.get_latest_posts(5)
    return render_template(
        'home/index.html',
        current_category=category_sub_name,
        posts=pagination.items,
        latest_posts=latest_posts,
        pagination=pagination,
    )
