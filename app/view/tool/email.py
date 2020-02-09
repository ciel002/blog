import html

from flask import request, json, render_template_string, render_template, session
from flask_login import current_user

from threading import Thread
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import mail
from app.function.verifycode import yzm, verify_email
from app.view.tool import tool


def generate_token(email, expiration=600):
    from manager import app
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'email': email}).decode(encoding='utf-8')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def update_mail_config():
    from manager import app
    from app.function.config import get_config
    app.config.update(
        MAIL_SERVER=get_config("web_mail_smtp_host"),
        MAIL_PORT=get_config("web_mail_smtp_port"),
        MAIL_USERNAME=get_config("web_mail_smtp_user"),
        MAIL_PASSWORD=get_config("web_mail_smtp_pass")
    )
    mail.init_app(app)


@tool.route('/send_sms_email/', methods=['GET', 'POST'])
def send_sms_email():
    update_mail_config()
    recipient = request.get_data().decode(encoding='utf-8')
    if not recipient:
        recipient = current_user.email
    if not verify_email(recipient):
        return json.dumps({
            "code": -1,
            "message": "请输入正确的邮箱格式"
        })
    try:
        # 配置邮件模板
        from manager import app
        from app.function.config import get_config
        code = yzm(6)
        session['sms_code'] = code
        html = render_template('common/email_sms.html', code=code)
        msg = Message(subject='郝明宸的个人博客来信', sender=get_config("web_mail_smtp_user"), recipients=[recipient],
                      html=html)
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
        return json.dumps({
            "code": 1,
            "message": "发送成功"
        })
    except Exception as e:
        return json.dumps({
            "code": -1,
            "message": "发送失败"
        })


@tool.route("/send_reset_password", methods=['GET', 'POST'])
def send_reset_password():
    update_mail_config()

    # 配置邮件模板
    template = html.unescape(get_config("MAIL_VALIDATION_TEMPLATE"))
    template = render_template_string(template, user=current_user, token=current_user.generate_token())

    msg = Message(subject='郝明宸的个人博客来信', sender=get_config("MAIL_SMTP_USER"), recipients=[current_user.email],
                  html=template)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return json.dumps({
        "code": 1,
        "message": "发送成功"
    })
