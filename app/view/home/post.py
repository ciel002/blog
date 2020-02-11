from flask import render_template, request, json, Response
from flask_login import current_user

from app import db
from app.model.cat import Category
from app.model.post import Post, PostComment, PostReply
from app.model.user import User
from app.view.home import home


@home.route('/post/<string:post_title>/')
def post(post_title):
    post = db.session.query(Post.id, Post.title, Post.create_time, User.name, Post.uid
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.content).filter(Post.uid == User.id
                                                 , Post.category_id == Category.id,
                                                 Post.title == post_title).first()
    comments_replies = PostComment.get_post_comments_and_replies(post.id)
    return render_template('home/post.html', post=post, comments_replies=comments_replies)


@home.route('/post/add_comment/', methods=['GET', 'POST'])
def add_post_comment():
    if request.method == 'POST':
        pid = request.args.get('pid')
        content = request.values.get("content")
        comment = PostComment(uid=current_user.id, pid=pid, content=content)
        comment.add_one()
        if comment.id:
            comments_replies = PostComment.get_post_comments_and_replies(pid)
            data = render_template('home/comment_list.html', comments_replies=comments_replies)
            return Response(json.dumps({'code': 1, 'msg': '评论成功', 'data': data}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': '评论失败'}), content_type='application/json')


@home.route('post/add_reply/', methods=['GET', 'POST'])
def add_comment_reply():
    if request.method == 'POST':
        pid = request.args.get('pid')
        print(pid)
        uid_a = request.values.get("uid_a")
        uid_b = request.values.get("uid_b")
        cid = request.values.get("cid")
        content = request.values.get("content")
        reply = PostReply(uid=uid_a, rid=uid_b, cid=cid, content=content)
        reply.add_one()
        if reply.id:
            comments_replies = PostComment.get_post_comments_and_replies(pid)
            data = render_template('home/comment_list.html', comments_replies=comments_replies)
            return Response(json.dumps({'code': 1, 'msg': '回复成功', 'data': data}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': '回复失败'}), content_type='application/json')
    return Response(json.dumps({'code': 0, 'msg': '回复失败'}), content_type='application/json')
