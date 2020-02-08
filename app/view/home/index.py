from flask import render_template

from app.function.paginate import get_home_index_paginate
from app.model.cat import Category
from app.model.post import Post
from app.view.home import home


@home.route('/')
@home.route('/list/<int:page>')
def index(page=1):
    from app.function.config import get_config
    categories = Category.get_all_categories()
    pagination = get_home_index_paginate(page=page, per_page=int(get_config("web_home_posts_pages")))
    latest_posts = Post.get_latest_posts(limit=3)
    return render_template('home/index.html', categories=categories, posts=pagination.items
                           , latest_posts=latest_posts, pagination=pagination, current_index='index')
