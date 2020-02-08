from functools import wraps
from flask import abort
from flask_login import current_user

from app.common.constant import GROUP_SUPERUSER


# 如果有访问某个页面的权限，则可以访问否则无法访问该页面
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if not current_user.is_authenticated:
            #     abort(403)
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# 特定超级管理员，其实没什么用
def admin_required(f):
    return permission_required(GROUP_SUPERUSER)(f)
