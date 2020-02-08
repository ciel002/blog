from flask import render_template
from flask_login import login_required

from . import admin
from app.function.navigation import get_navigation_info
from app.function.permissions import permission_required
from app.model.post import Post, PostComment
from app.model.user import User


@admin.route("/")
@login_required
@permission_required(1)
def index():
    posts_count = Post.get_posts_count()
    comments_count = PostComment.get_comments_count()
    users_count = User.get_users_count(0)
    context = {
        'posts_count': posts_count,
        'comments_count': comments_count,
        'users_count': users_count,
    }
    navigation = get_navigation_info(title="仪表盘", sub_title="控制器", tag="index")
    return render_template("admin/index.html", navigation=navigation, context=context)