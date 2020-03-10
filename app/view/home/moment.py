from flask import render_template, request, Response, json

from app.model.moment import Moment
from app.model.post import Post
from app.view.home import home


@home.route('/moment/', methods=['GET', 'POST'])
def moment(page=1):
    """
    动态列表页面
    :return:
    """
    if request.method == 'GET':
        moments = Moment.get_moments(page=page, limit=10)
        latest_posts = Post.get_latest_posts(5)
        return render_template("home/moment.html", moments=moments, latest_posts=latest_posts)


@home.route('ajax_moment', methods=['GET', 'POST'])
def ajax_moment():
    """
    通过ajax方式加载更多的动态信息
    :return:
    """
    if request.method == 'POST':
        page = int(request.args.get('page'))
        moments = Moment.get_moments(page=page, limit=10)
        if moments:
            data = render_template("home/moment_list.html", moments=moments)
            return Response(json.dumps({'code': 1, 'msg': '加载成功', 'data': data}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': '已经到最后了'}), content_type='application/json')
