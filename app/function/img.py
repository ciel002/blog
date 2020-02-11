import hashlib
import os

from PIL import Image, ImageFont, ImageDraw
from werkzeug.utils import secure_filename
from app.model.user import UserAvatar


def md5_file(file):
    name = secure_filename(file.filename)
    length = str(len(file.read()))
    file.seek(0, 0)
    m5 = hashlib.md5((name + length).encode('utf-8'))
    return m5.hexdigest()


def water_mark(filepath, mark=u'@ 郝明宸的个人博客'):
    image = Image.open(filepath)
    from app.function.config import get_config
    ttf_path = os.path.join(get_config("web_system_font_path"), 'alibaba.ttf')
    font = ImageFont.truetype(ttf_path, size=18)
    layer = image.convert('RGBA')  # 将图像转为RGBA图像
    # 生成同等大小的图片
    text_overlay = Image.new('RGBA', layer.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)  # 画图
    # 获取文本大小
    text_size_x, text_size_y = image_draw.textsize(mark, font=font)
    # 设置文本文字位置
    text_xy = (layer.size[0] - text_size_x, layer.size[1] - text_size_y)
    image_draw.text(text_xy, mark, font=font, fill=(47, 79, 79, 100))
    # 将新生成的图片覆盖到需要加水印的图片上
    after = Image.alpha_composite(layer, text_overlay)
    after.save(filepath)
