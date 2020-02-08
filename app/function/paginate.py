from sqlalchemy import func

from app import db
from app.common.constant import STATUS_PUBLISH, PROPERTY_PUBLIC
from app.model.cat import Category
from app.model.group import UserGroup
from app.model.post import Post, PostComment, PostReply
from app.model.setting import Status, Property
from app.model.user import User


def get_home_index_paginate(page, per_page):
    return db.session.query(Post.title, Post.create_time, User.name
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.abstract).filter(Post.uid == User.id
                                                  , Post.category_id == Category.id,
                                                  Post.post_property == PROPERTY_PUBLIC
                                                  , Post.status == STATUS_PUBLISH).order_by(
        Post.create_time.desc()).paginate(page=page, per_page=per_page)


def get_home_category_paginate(page, per_page, category_sub_name):
    return db.session.query(Post.title, Post.create_time, User.name
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.abstract).filter(Post.uid == User.id
                                                  , Post.category_id == Category.id,
                                                  Post.post_property == PROPERTY_PUBLIC
                                                  , Post.status == STATUS_PUBLISH,
                                                  Category.sub_name == category_sub_name).order_by(
        Post.create_time.desc()).paginate(page=page, per_page=per_page)


def get_home_search_paginate(page, per_page, query):
    return db.session.query(Post.title, Post.create_time, User.name
                            , Category.name.label('category_name'), Category.sub_name.label('category_sub_name'),
                            Post.abstract).filter(Post.uid == User.id
                                                  , Post.category_id == Category.id,
                                                  Post.post_property == PROPERTY_PUBLIC
                                                  , Post.status == STATUS_PUBLISH,
                                                  Post.title.ilike('%%%s%%' % query)).order_by(
        Post.create_time.desc()).paginate(page=page, per_page=per_page)


def get_admin_posts_paginate(page, per_page, status=STATUS_PUBLISH):
    return db.session.query(Post.id, Post.title, User.name.label('username'), Post.create_time, Category.name,
                            func.count(PostComment.pid).label('comment_total')
                            , Post.last_visited_time,
                            Status.name.label('status_name')
                            , Property.name.label('property_name')).outerjoin(PostComment,
                                                                              Post.id == PostComment.pid).filter(
        Post.status == status,
        Post.uid == User.id
        , Post.category_id == Category.id,
        Post.status == Status.id
        , Post.post_property == Property.id).group_by(Post.id).paginate(page=page, per_page=per_page)


def get_admin_users_paginate(page, per_page, gid):
    from app.model.post import Post, PostComment
    if int(gid) == 0:
        table4 = db.session.query(User.id, User.name, UserGroup.name.label('groupname')
                                  , User.register_time, User.last_login_time, User.email, User.wechat,
                                  User.deletable
                                  , func.count(PostComment.uid).label('comment_total'), User.deletable).outerjoin(
            PostComment,
            User.id == PostComment.uid).filter(
            UserGroup.id == User.group_id).group_by(User.id).subquery()
    else:
        table4 = db.session.query(User.id, User.name, UserGroup.name.label('groupname')
                                  , User.register_time, User.last_login_time, User.email, User.wechat,
                                  User.deletable
                                  , func.count(PostComment.uid).label('comment_total'), User.deletable).outerjoin(
            PostComment,
            User.id == PostComment.uid).filter(
            UserGroup.id == User.group_id, UserGroup.id == gid).group_by(User.id).subquery()
    results = db.session.query(table4.c.id, table4.c.name, table4.c.groupname, table4.c.register_time,
                               table4.c.last_login_time, func.count(Post.uid).label('post_total'),
                               table4.c.comment_total, table4.c.email, table4.c.wechat,
                               table4.c.deletable).outerjoin(
        Post, Post.uid == table4.c.id).group_by(table4.c.id).paginate(page=page, per_page=per_page)
    return results


def get_admin_comments_paginate(page, per_page ,status):
    return db.session.query(PostComment.id, User.name, PostComment.content,
                            Post.title, PostComment.status).filter(
        PostComment.status == status, User.id == PostComment.uid, Post.id == PostComment.pid).order_by(
        PostComment.create_time.desc()).paginate(page=page, per_page=per_page)


def get_admin_post_replies_paginate(page, per_page ,status):
    return db.session.query(PostReply.id, User.name, PostReply.content,
                            PostComment.id.label("cid"), PostReply.status).filter(
        PostReply.status == status, User.id == PostReply.uid, PostComment.id == PostReply.cid).order_by(
        PostReply.create_time.desc()).paginate(page=page, per_page=per_page)
