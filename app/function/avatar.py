import os

from PIL import Image
from werkzeug.utils import secure_filename

from app.function.img import md5_file


def alter_avatar(file, uid):
    from app.function.config import get_config
    # 获取安全的文件名，用于保存
    name = secure_filename(file.filename)
    ext = os.path.splitext(name)[-1]
    import uuid
    filename = uuid.uuid4().hex + ext
    # 计算文件的MD5，防止重复保存
    md5 = md5_file(file)
    # 文件的保存路径
    path = get_config("web_system_upload_avatar_path")
    if not os.path.exists(path):
        os.mkdir(path)
    # 文件的保存路径
    file.save(os.path.join(path, filename))
    # 需要保存什么大小的头像
    sizes = {
        "s" + filename: 80,
        "m" + filename: 160,
        "b" + filename: 250
    }
    # 对头像进行裁剪和缩放
    return resize_avatar(os.path.join(path, filename), path, uid, sizes)


def resize_avatar(img, path, uid, sizes):
    sImg = Image.open(img)
    sImg.convert('RGBA')

    # 删除原数据库中该用户的头像
    from app import db
    from app.model.user import UserAvatar, User
    avatars = UserAvatar.query.filter_by(uid=uid).all()
    for i in avatars:
        db.session.delete(i)
    db.session.commit()

    try:
        for name, value in sizes.items():
            # 生成缩放后的图片，并保存到本地和数据库中
            dImg = sImg.resize((value, value), Image.ANTIALIAS)
            filepath = os.path.join(path, name)
            dImg.save(filepath)
            avatar = UserAvatar(uid=uid, name=name, path=path)
            avatar.add_one()
        user = User.query.filter_by(id=uid).first()
        user.avatar = 1
        db.session.commit()
        return True
    except Exception as e:
        return False
