import time

from sqlalchemy import func
from sqlalchemy.orm import aliased

from app import db
from app.common.constant import TABLE_PREFIX, PROPERTY_PRIVATE, STATUS_DRAFT, STATUS_DELETED, STATUS_PUBLISH
from app.function.model import get_dict_list_from_result
from app.model.cat import Category
from app.model.user import User


class Post(db.Model):
    __tablename__ = TABLE_PREFIX + 'posts'
    id = db.Column(db.Integer, primary_key=True)  # 文章ID
    title = db.Column(db.String(50), unique=True, nullable=False)  # 文章标题
    abstract = db.Column(db.Text, nullable=False)  # 文章摘要
    content = db.Column(db.Text, nullable=False)  # 文章内容
    uid = db.Column(db.Integer, nullable=False)  # 作者
    create_time = db.Column(db.DateTime)  # 文章创建时间
    update_time = db.Column(db.DateTime)  # 文章最近的更新时间
    category_id = db.Column(db.Integer, nullable=False)  # 文章分类
    rank = db.Column(db.Integer, default=0)  # 文章排名
    is_top = db.Column(db.Boolean, default=False)  # 文章是否置顶显示
    visited_total = db.Column(db.Integer, default=0)  # 访问次数
    first_visited_time = db.Column(db.DateTime)  # 文章第一次访问的时间
    last_visited_time = db.Column(db.DateTime)  # 文章最后一次访问的时间
    post_property = db.Column(db.Integer, nullable=False, default=PROPERTY_PRIVATE)  # 文章属性
    status = db.Column(db.Integer, nullable=False, default=STATUS_DRAFT)  # 文章状态

    def __init__(self, title=None, abstract=None, content=None, uid=None, category_id=None
                 , rank=None, is_top=None, visited_total=None, post_property=None, status=None):
        self.title = title
        self.abstract = abstract
        self.content = content
        self.uid = uid
        self.category_id = category_id
        self.rank = rank
        self.is_top = is_top
        self.visited_total = visited_total
        self.comment_total = 0
        self.visited_total = 0
        self.post_property = post_property
        self.status = status
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Post %r>' % self.username

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_post(self, title, abstract, uid, content, category_id
                    , rank, is_top, post_property, status):
        self.title = title
        self.abstract = abstract
        self.uid = uid
        self.content = content
        self.category_id = category_id
        self.rank = rank
        self.is_top = is_top
        self.post_property = post_property
        self.status = status
        self.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        db.session.commit()

    def delete(self):
        self.status = STATUS_DELETED
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_posts_count(status=STATUS_PUBLISH):
        return db.session.query(func.count(Post.id)).filter(Post.status == status).scalar()

    @staticmethod
    def get_posts_info(status):
        from app.model.cat import Category
        from app.model.user import User
        from app.model.setting import Status, Property
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
            , Post.post_property == Property.id).group_by(Post.id).all()

    @staticmethod
    def get_posts_info_by_user(uid):
        subquery_comment = db.session.query(func.count(PostComment.id)).filter(
            PostComment.pid == Post.id).correlate(
            Post).as_scalar()
        subquery_reply = db.session.query(func.count(PostReply.id)).filter(
            PostReply.cid == PostComment.id, PostComment.pid == Post.id).correlate(
            PostComment, Post).as_scalar()
        result = db.session.query(Post.id, Post.title, Category.name, Category.sub_name, Post.status, Post.create_time,
                                  subquery_comment.label('comment_count'),
                                  subquery_reply.label('reply_count')).filter(Category.id == Post.category_id,
                                                                              Post.uid == uid).all()
        return result

    @staticmethod
    def get_latest_posts(limit):
        return db.session.query(Post.title).filter(Post.status == STATUS_PUBLISH).order_by(
            Post.create_time.desc()).limit(
            limit).all()


class PostReply(db.Model):
    __tablename__ = TABLE_PREFIX + 'post_reply'
    id = db.Column(db.Integer, primary_key=True)  # 文章回复ID
    cid = db.Column(db.Integer, nullable=False)  # 文章评论ID
    uid = db.Column(db.Integer, nullable=False)  # 文章回复者ID
    rid = db.Column(db.Integer, nullable=False)  # 文章被回复者ID, 如果rid为0，表示第一个回复该评论
    content = db.Column(db.Text, nullable=False)  # 文章评论内容
    status = db.Column(db.Integer)  # 文章评论状态
    create_time = db.Column(db.DateTime)  # 文章评论创建时间

    def __init__(self, uid=None, cid=None, rid=None, content=None, status=STATUS_PUBLISH):
        self.cid = cid
        self.content = content
        self.uid = uid
        self.rid = rid
        self.status = status
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Comment %r>' % self.id

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_status(self, status):
        self.status = status
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_replies_of_comment(cid):
        a = aliased(User)
        b = aliased(User)
        replies = db.session.query(PostReply.id, PostReply.uid, PostReply.content, PostReply.create_time,
                                            PostReply.cid,
                                            PostReply.rid, a.name.label('uname'), b.name.label('rname')).filter(
            a.id == PostReply.uid, b.id == PostReply.rid,
            PostReply.cid == PostComment.id, PostReply.cid==cid).order_by(
            PostReply.create_time.desc()).all()
        return replies


class PostComment(db.Model):
    __tablename__ = TABLE_PREFIX + 'post_comment'
    id = db.Column(db.Integer, primary_key=True)  # 文章评论ID
    uid = db.Column(db.Integer, nullable=False)  # 文章评论者ID
    pid = db.Column(db.Integer, default=0)  # 文章评论文章ID
    content = db.Column(db.Text, nullable=False)  # 文章评论内容
    status = db.Column(db.Integer)  # 文章评论状态
    create_time = db.Column(db.DateTime)  # 文章评论创建时间

    def __init__(self, uid=None, content=None, pid=None, status=STATUS_PUBLISH):
        self.content = content
        self.uid = uid
        self.pid = pid
        self.status = status
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __repr__(self):
        return '<Comment %r>' % self.id

    def add_one(self):
        db.session.add(self)
        db.session.commit()

    def update_status(self, status):
        self.status = status
        db.session.commit()

    def real_delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_post_comments(pid):
        return db.session.query(PostComment.id, User.name, User.avatar, PostComment.create_time,
                                PostComment.content, PostComment.uid).filter(
            PostComment.pid == pid, PostComment.status == STATUS_PUBLISH, PostComment.uid == User.id).order_by(
            PostComment.create_time.desc()).all()

    @staticmethod
    def get_post_comments_and_replies(pid):
        comments = db.session.query(PostComment.id, User.name, User.avatar, PostComment.create_time,
                                    PostComment.content, PostComment.uid).filter(
            PostComment.pid == pid, PostComment.status == STATUS_PUBLISH, PostComment.uid == User.id).order_by(
            PostComment.create_time.desc()).all()
        comments_list = get_dict_list_from_result(comments)
        for comment in comments_list:
            replies = PostReply.query_replies_of_comment(comment['id'])
            comment['replies'] = replies
        return comments_list

    @staticmethod
    def get_comments_count():
        return db.session.query(func.count(PostComment.id)).scalar()


