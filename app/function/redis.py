from functools import wraps

from app import redis


def increase_explore_count(func):
    """
    自增网页访问数
    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        redis.incr('blog_explore_count')
        return func(*args, **kwargs)

    return decorator


def get_explore_count():
    """
    :return: 网站访问数
    """
    return redis.get('blog_explore_count')


def increase_explore_post_count(pid):
    """
    当有用户访问文章时，增加该文章的访问数
    :param pid:
    :return:
    """
    redis.hincrby('blog_explore_post_count', 'pid:'+str(pid), 1)


def get_explore_post_count(pid):
    """
    返回该文章ID对应文章的访问数
    :param pid: 文章ID
    :return: 返回文章访问数
    """
    return redis.hget('blog_explore_post_count', 'pid:'+str(pid))