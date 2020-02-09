from flask import render_template, redirect, url_for

from app.view.home import home


@home.errorhandler(401)
def have_not_login(error):
    return redirect(url_for("home.index")), 401


@home.errorhandler(404)
def handle_404_error(error):
    return render_template('home/page_not_found.html', message=error), 404


@home.errorhandler(500)
def handle_500_error(error):
    return render_template('home/internal_server_error.html', message=error), 500
