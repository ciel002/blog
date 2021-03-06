from flask import render_template

from app.function.paginate import get_home_index_paginate
from app.function.redis import increase_explore_count
from app.model.post import Post
from app.view.home import home


@home.route('/')
@home.route('/list/<int:page>')
@increase_explore_count
def index(page=1):
    from app.function.config import get_config
    pagination = get_home_index_paginate(page=page, per_page=int(get_config("web_home_posts_pages")))
    latest_posts = Post.get_latest_posts(limit=3)
    return render_template('home/index.html', posts=pagination.items
                           , latest_posts=latest_posts, pagination=pagination, current_index='index')
