from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user, login_user

from app.model.cat import Category
from app.view.home import home


@home.route("user/<user_name>/<tag>")
@login_required
def user(user_name, tag):
    categories = Category.get_all_categories()
    return render_template("home/user.html", tag=tag, categories=categories)


@home.route("user/upload", methods=["GET", "POST"])
def upload():
    file = request.files['img']
    return redirect(url_for("home.user", user_name=current_user.name, tag="overview"))


@home.route("user/forget_password")
def forget_password_request():
    return "forget_password"


# @home.route("user/forget_password/<string:token>", methods=['GET', 'POST'])
# def reset_password(token):
#     form = ResetPasswordForm()
#     if request.method == 'GET':
#         return render_template('home/reset_password.html', form=form)
#     if request.method == 'POST' and form.validate_on_submit():
#         new_password = form.inputPassword.data
#         User.reset_password(token, new_password=new_password)
#         login_user(user)
#         return redirect(url_for("home.index"))
