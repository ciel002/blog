from flask import render_template, redirect, url_for, request, current_app, Response, json, session
from flask_login import login_required, current_user, login_user

from app.forms.home.user import ResetPasswordForm, ResetEmailForm
from app.model.post import Post
from app.model.user import User
from app.view.home import home


@home.route("user/")
@home.route("user/info/")
@login_required
def user():
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/alter_password/")
@login_required
def alter_password():
    form = ResetPasswordForm()
    return render_template("home/user_alter_password.html", form=form)


@home.route("user/alter_email/")
@login_required
def alter_email():
    form = ResetEmailForm()
    return render_template("home/user_alter_email.html", form=form)


@home.route("user/my_posts/")
@login_required
def my_posts():
    posts = Post.get_posts_info_by_user(current_user.id)
    print(posts[0].keys())
    return render_template("home/user_my_posts.html", user=user, posts=posts)


@home.route("user/my_comments/")
@login_required
def my_comments():
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/my_replies/")
@login_required
def my_replies():
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/forget_password/")
def forget_password_request():
    return "forget_password"


@home.route("user/reset_password/", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if request.method == 'POST':
        if not form.validate():
            return Response(json.dumps({'code': 0, 'msg': form.get_first_error()}), content_type='application/json')
        if not session.get('sms_code').lower() == form.SmsCode.data.lower():
            return Response(json.dumps({'code': 0, 'msg': "邮箱验证码不正确"}), content_type='application/json')
        if current_user.reset_password(new_password=form.Password.data):
            session.pop('sms_code')
            return Response(json.dumps({'code': 1, 'msg': '修改成功'}), content_type='application/json')
    return Response(json.dumps({'code': 0, 'msg': '修改密码失败，请联系管理员'}), content_type='application/json')


@home.route("user/reset_email/", methods=['GET', 'POST'])
@login_required
def reset_email():
    form = ResetEmailForm()
    print(session)
    if request.method == 'POST':
        if not form.validate():
            return Response(json.dumps({'code': 0, 'msg': form.get_first_error()}), content_type='application/json')
        if not session.get('sms_code').lower() == form.SmsCode.data.lower():
            return Response(json.dumps({'code': 0, 'msg': "邮箱验证码不正确"}), content_type='application/json')
        if current_user.reset_email(new_email=form.NewEmail.data):
            session.pop('sms_code')
            return Response(json.dumps({'code': 1, 'msg': '修改成功, 2秒后刷新页面'}), content_type='application/json')
        else:
            return Response(json.dumps({'code': 0, 'msg': '邮箱已绑定，请更换邮箱'}), content_type='application/json')
    return Response(json.dumps({'code': 0, 'msg': '修改密码失败，请联系管理员'}), content_type='application/json')
