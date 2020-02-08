from flask import render_template

from app.view.home import home


@home.app_errorhandler(404)
def handle_404_error(error):
    return render_template('home/page_not_found.html', message=error), 404


@home.app_errorhandler(500)
def handle_500_error(error):
    return render_template('home/internal_server_error.html', message=error), 500