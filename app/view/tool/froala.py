import os

from flask import request, make_response, json, url_for, current_app
from werkzeug.utils import secure_filename

from app import db
from app.common.constant import DEFAULT_ALBUM
from app.function.img import water_mark, md5_file
from app.model.picture import Picture
from app.view.tool import tool


@tool.route('/froala/upload_image/', methods=['GET', 'POST'])
def upload_image_froala():
    """
    获取由froala上传的图片文件
    将图片重命名保存到本地
    :return: json格式
    """
    if request.method == 'POST':
        file = request.files['file']
        if file:
            md5 = md5_file(file)
            name = secure_filename(file.filename)
            ext = os.path.splitext(name)[1]
            import uuid
            filename = uuid.uuid4().hex + ext
            picture = db.session.query(Picture.filename).filter(Picture.md5 == md5).first()
            if not picture:
                from app.function.config import get_config
                filepath = get_config('web_system_upload_image_froala_path')
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                path = os.path.join(filepath, filename)
                file.save(path)
                water_mark(path)
                picture = Picture(name=name, filename=filename, album_id=DEFAULT_ALBUM, md5=md5, description='froala编辑器图片上传')
                picture.add_one()
            link_path = url_for('tool.load_image_froala', filename=picture.filename)
            return json.dumps({"link": link_path})


@tool.route('/froala/load_image/<string:filename>/', methods=['GET', 'POST'])
def load_image_froala(filename):
    if request.method == "GET":
        from app.function.config import get_config
        file_dir = os.path.join(get_config('web_system_upload_image_froala_path'))
        if filename is not None:
            image_data = open(os.path.join(file_dir, '%s' % filename), 'rb').read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    return filename


@tool.route('/froala/upload_video/', methods=['GET', 'POST'])
def upload_video_froala():
    """
    获取由froala上传的图片文件
    将图片重命名保存到本地
    :return: json格式
    """
    if request.method == 'POST':
        file = request.files['file']
        if file:
            md5 = md5_file(file)
            name = secure_filename(file.filename)
            ext = os.path.splitext(name)[1]
            filename = md5 + ext
            picture = db.session.query(Picture.filename).filter(Picture.md5 == md5).first()
            if not picture:
                from app.function.config import get_config
                path = os.path.join(get_config('FROALA_UPLOADS_PATH'), filename)
                file.save(path)
                water_mark(path)
                picture = Picture(name=name, filename=filename, album_id=DEFAULT_ALBUM, md5=md5, description='froala')
                picture.add_one()
            link_path = url_for('imgs.load_image_froala', filename=picture.filename)
            return json.dumps({"link": link_path})


@tool.route('/froala/load_video/<string:filename>/', methods=['GET', 'POST'])
def load_video_froala(filename):
    if request.method == "GET":
        from app.function.config import get_config
        file_dir = os.path.join(current_app.config['BASEDIR'], get_config('FROALA_UPLOADS_PATH'))
        if filename is not None:
            image_data = open(os.path.join(file_dir, '%s' % filename), 'rb').read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    return filename
