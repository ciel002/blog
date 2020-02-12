from flask import url_for, render_template, flash, request, session
from flask_login import logout_user, login_required, login_user
from werkzeug.utils import redirect

from app.form.admin.login import LoginForm
from app.model.user import User
from app.view.admin import admin


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(form.Email)
        print(form.Password)
        print(form.VerifyCode)
        print(session.get('verify_code').lower())
        if form.validate_on_submit() and session.get('verify_code').lower() == form.VerifyCode.data.lower():
            user = User.query.filter_by(email=form.Email.data).first()
            if user is None:
                flash('not exist')
                return redirect(url_for('admin.login'))
            if user.check_hash_password(password=form.Password.data):
                login_user(user)
                return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))
