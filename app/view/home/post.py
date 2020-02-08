from flask import render_template, request, json
from flask_login import current_user

from app import db
from app.model.cat import Category
from app.model.post import Post, PostComment
from app.model.user import User
from app.view.home import home


@home.route('/post/<string:post_title>/')
def post(post_title):
    post = db.session.query(Post.id, Post.title, Post.create_time, User.name
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.content).filter(Post.uid == User.id
                                                 , Post.category_id == Category.id,
                                                 Post.title == post_title).first()
    post_comment = PostComment.get_post_comments(post.id)
    categories = Category.query.all()
    return render_template('home/post.html', categories=categories, post=post, post_comment=post_comment)


@home.route('/post/add_comment/<int:pid>', methods=['GET', 'POST'])
def add_post_comment(pid):
    if request.method == 'POST':
        content = request.values.get("content")
        comment = PostComment(uid=current_user.id, pid=pid, content=content)
        comment.add_one()
        if comment.id:
            post_comment = PostComment.get_post_comments(pid)
            data = render_template('home/comment_list.html', post_comment=post_comment)
            return json.dumps({
                "code": 1,
                "msg": "出错",
                "data": data,
            })
        return json.dumps({
            "code": 0,
            "msg": "出错",
        })
