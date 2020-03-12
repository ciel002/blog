from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config, Redis

db = SQLAlchemy()
migrate = Migrate(db)
mail = Mail()
login_manager = LoginManager()
redis = Redis.connect()


# 将创建app的动作封装成一个函数
def create_app(config_name):
    # 创建app实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config.get(config_name) or 'default')
    # 执行额外的初始化
    config.get(config_name).init_app(app)

    # 注册蓝图路由
    from app.view.admin import admin as admin_blueprint
    from app.view.home import home as home_blueprint
    from app.view.tool import tool as tool_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(tool_blueprint, url_prefix="/tool")

    # 设置debug=True,让toolbar生效
    # app.debug=True

    # 加载数据库
    db.init_app(app)
    migrate.init_app(app, db)
    # 加载邮件插件
    mail.init_app(app)
    # 加载用户登录插件
    login_manager.init_app(app)

    # 定义全局函数
    from app.function.redis import get_explore_post_count
    app.add_template_global(get_explore_post_count, 'get_explore_post_count')

    # 返回app实例对象
    app.app_context().push()
    return app