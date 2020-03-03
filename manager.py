# 入口文件
import os

from flask_migrate import MigrateCommand

from app import create_app, db
from flask_script import Server, Manager

# 通过FLASK_CONFIG选择配置项
config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 生成app
app = create_app(config_name)

# 导入所有模型
from app.model import *

# 导入公共函数
from app.function import *


# APP整体上下文配置环境
@app.context_processor
def my_context_processor():
    from app.model.setting import Config
    from app.model.cat import Category
    return dict(
        web_config=Config.get_config(),
        categories=Category.get_all_categories(),
    )


manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=8091, use_debugger=True, use_reloader=True))
manager.add_command("db", MigrateCommand)


# 初始化数据库
@manager.command
def init_database():
    from app.data import init_database
    init_database()


if __name__ == '__main__':
    try:
        import sys

        # sys.exit(manager.run())
        manager.run()
    except Exception as e:
        import traceback

        traceback.print_exc()
