from flask import render_template, request

from app.function.paginate import get_home_search_paginate
from app.function.redis import increase_explore_count
from app.model.post import Post
from app.view.home import home


@home.route('/search')
@increase_explore_count
def search(page=1):
    from app.function.config import get_config
    pagination = get_home_search_paginate(page=page, per_page=int(get_config("web_home_posts_pages")),
                                          query=request.args.get('query'))
    latest_posts = Post.get_latest_posts(5)
    return render_template('home/index.html', posts=pagination.items, latest_posts=latest_posts,
                           pagination=pagination, current_index='index')
