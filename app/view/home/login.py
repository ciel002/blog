from flask import url_for, redirect, request, session, flash, render_template, json, Response
from flask_login import login_user, login_required, logout_user

from app.common.constant import GROUP_USER
from app.forms.home.login import LoginForm, RegisterForm
from app.model.user import User
from app.view.home import home


@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        verify = session['verify_code'].lower() == form.VerifyCode.data.lower()
        if not form.validate():
            return Response(json.dumps({'code': 0, 'msg': form.get_first_error()}), content_type='application/json')
        if verify:
            user = User.query.filter_by(email=form.Email.data).first()
            if user is None or not user.is_authenticated:
                return Response(json.dumps({'code': 0, 'msg': '用户名不存在'}), content_type='application/json')
            if user.check_hash_password(form.Password.data):
                login_user(user)
                return Response(json.dumps({'code': 1, 'msg': '登录成功'}), content_type='application/json')
            else:
                return Response(json.dumps({'code': 0, 'msg': '用户名或密码不正确'}), content_type='application/json')
        return Response(json.dumps({'code': 0, 'msg': "验证码不正确"}), content_type='application/json')


@home.route("/modal_login/")
def modal_login():
    form = LoginForm()
    return render_template("home/modal_login.html", loginForm=form)


@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if not form.validate():
            return Response(json.dumps({'code': 0, 'msg': form.get_first_error()}), content_type='application/json')
        if not session['verify_code'].lower() == form.VerifyCode.data.lower():
            return Response(json.dumps({'code': 0, 'msg': "验证码不正确"}), content_type='application/json')
        if not session[form.Email.data].lower() == form.SmsCode.data.lower():
            return Response(json.dumps({'code': 0, 'msg': "邮箱验证码不正确"}), content_type='application/json')
        user = User.query.filter_by(email=form.Email.data).first()
        if user is not None:
            return Response(json.dumps({'code': 0, 'msg': "用户已经存在"}), content_type='application/json')
        else:
            new_user = User(name=form.Name.data, password=form.Password.data,
                            email=form.Email.data)
            new_user.add_one()
            login_user(new_user)
            session.pop(form.Email.data)
            return Response(json.dumps({'code': 1, 'msg': '注册成功'}), content_type='application/json')


@home.route("/modal_register/")
def modal_register():
    form = RegisterForm()
    return render_template("home/modal_register.html", registerForm=form)


@home.route("/logout/", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    if "user" not in request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for("home.index"))
