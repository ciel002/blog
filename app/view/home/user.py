from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user, login_user

from app.model.cat import Category
from app.model.user import User
from app.view.home import home


@home.route("user/")
@home.route("user/info/")
@login_required
def user():
    categories = Category.get_all_categories()
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/alter_password/")
@login_required
def alter_password():
    categories = Category.get_all_categories()
    user = User.get_user_info(current_user.id)
    return render_template("home/alter_password.html")


@home.route("user/my_posts/")
@login_required
def my_posts():
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/my_comments/")
@login_required
def my_comments():
    user = User.get_user_info(current_user.id)
    return render_template("home/user.html", user=user)


@home.route("user/forget_password/")
def forget_password_request():
    return "forget_password"


@home.route("user/forget_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if request.method == 'GET':
        return render_template('home/reset_password.html', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        new_password = form.inputPassword.data
        User.reset_password(token, new_password=new_password)
        login_user(user)
        return redirect(url_for("home.index"))
