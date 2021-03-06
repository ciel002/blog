from flask import render_template, request, json, Response
from flask_login import current_user, login_required

from app import db
from app.function.redis import increase_explore_count, increase_explore_post_count
from app.model.cat import Category
from app.model.post import Post, PostComment, PostReply
from app.model.user import User
from app.view.home import home


@home.route('/post/<string:post_title>/')
@increase_explore_count
def post(post_title):
    post = db.session.query(Post.id, Post.title, Post.create_time, User.name, Post.uid
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.content).filter(Post.uid == User.id
                                                 , Post.category_id == Category.id,
                                                 Post.title == post_title).first()
    comments_replies = PostComment.get_post_comments_and_replies(post.id)
    increase_explore_post_count(post.id)
    return render_template('home/post.html', post=post, comments_replies=comments_replies)


@home.route('/post/add_comment/', methods=['GET', 'POST'])
@login_required
def add_post_comment():
    if request.method == 'POST':
        pid = request.args.get('pid')
        content = request.values.get("content")
        if not content.strip():
            return Response(json.dumps({'code': 0, 'msg': '评论内容不能为空'}), content_type='application/json')
        comment = PostComment(uid=current_user.id, pid=pid, content=content)
        comment.add_one()
        if comment.id:
            comments_replies = PostComment.get_post_comments_and_replies(pid)
            data = render_template('home/comment_list.html', comments_replies=comments_replies)
            return Response(json.dumps({'code': 1, 'msg': '评论成功', 'data': data}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': '评论失败'}), content_type='application/json')


@home.route('post/add_reply/', methods=['GET', 'POST'])
@login_required
def add_comment_reply():
    if request.method == 'POST':
        pid = request.args.get('pid')
        uid_a = request.values.get("uid_a")
        uid_b = request.values.get("uid_b")
        cid = request.values.get("cid")
        content = request.values.get("content")
        if not content.strip():
            return Response(json.dumps({'code': 0, 'msg': '回复内容不能为空'}), content_type='application/json')
        reply = PostReply(uid=uid_a, rid=uid_b, cid=cid, content=content)
        reply.add_one()
        if reply.id:
            comments_replies = PostComment.get_post_comments_and_replies(pid)
            data = render_template('home/comment_list.html', comments_replies=comments_replies)
            return Response(json.dumps({'code': 1, 'msg': '回复成功', 'data': data}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': '回复失败'}), content_type='application/json')
    return Response(json.dumps({'code': 0, 'msg': '回复失败'}), content_type='application/json')
