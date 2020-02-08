from io import BytesIO

from flask import make_response, session

from app.function.captcha import Captcha
from app.view.tool import tool


@tool.route("/captcha")
def graph_captcha():
    text, image = Captcha.gen_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    session['verify_code'] = text
    return resp
