from app import db
from app.common.constant import DELETABLE_NO, STATUS_USEFUL, GROUP_SUPERUSER
from app.model.auth import GroupAuthority
from app.model.group import UserGroup
from app.model.setting import Status, Property, Config
from app.model.user import User


def init_database():
    # 初始文章是否为个人隐私
    private = Property("私有", DELETABLE_NO, "")
    public = Property("公有", DELETABLE_NO, "")

    # 初始文章或设置状态值
    draft = Status("草稿", DELETABLE_NO, "")
    publish = Status("发布", DELETABLE_NO, "")
    deleted = Status("删除", DELETABLE_NO, "")
    useful = Status("正在使用", DELETABLE_NO, "")
    useless = Status("未使用", DELETABLE_NO, "")

    # 初始用户组，方便权限管理
    supergroup = UserGroup("超级管理员", STATUS_USEFUL, "1,2,3,4,5", DELETABLE_NO)
    manager = UserGroup("普通管理员", STATUS_USEFUL, "1,2,3,4,5", DELETABLE_NO)
    viper = UserGroup("普通会员", STATUS_USEFUL, "1,2,3,4,5", DELETABLE_NO)
    user = UserGroup("用户", STATUS_USEFUL, "1,2,3,4,5", DELETABLE_NO)
    visitor = UserGroup("游客", STATUS_USEFUL, "1,2,3,4,5", DELETABLE_NO)

    # 初始超级用户
    superuser = User("Ciel", "lingciel2002", GROUP_SUPERUSER, "18633568630", "1102839480@qq.com", "", "",
                     deletable=DELETABLE_NO)

    """
    初始配置项
    1.前台页面配置
    2.后台页面配置
    3.邮件配置
    4.上传配置
    """
    # 1 前台页面配置
    web_home_title = Config("首页窗口标题", "web_home_title", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    web_home_logo_title = Config("首页LOGO标题", "web_home_logo_title", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    web_home_footer_name = Config("首页底部标题", "web_home_footer_name", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    web_home_footer_signature = Config("首页底部签名", "web_home_footer_signature", "博客底部签名", "", 0, STATUS_USEFUL)
    web_home_posts_pages = Config("主页每页文章数", "web_home_posts_pages", "10", "", 0, STATUS_USEFUL)
    # 2 后台页面配置
    web_admin_title = Config("后台窗口标题", "web_admin_title", "后台管理", "", 0, STATUS_USEFUL)
    web_admin_logo_title = Config("后台LOGO标题", "web_admin_logo_title", "后台管理", "", 0, STATUS_USEFUL)
    web_admin_post_per_page = Config("后台每页文章数", "web_admin_post_per_page", "后台管理", "", 0, STATUS_USEFUL)
    web_admin_user_per_page = Config("后台每页用户数", "web_admin_user_per_page", "后台管理", "", 0, STATUS_USEFUL)
    web_admin_comment_per_page = Config("后台每页评论数", "web_admin_comment_per_page", "后台管理", "", 0, STATUS_USEFUL)
    web_admin_comment_reply_per_page = Config("后台每页评论回复数", "web_admin_comment_reply_per_page", "后台管理", "", 0,
                                              STATUS_USEFUL)
    web_admin_site_copy = Config("后台版权信息", "web_admin_site_copy", "郝明宸", "", 0, STATUS_USEFUL)
    web_admin_site_version = Config("网站版本信息", "web_admin_site_version", "1.10", "", 0, STATUS_USEFUL)
    # 3 邮件配置
    mail_smtp_host = Config("邮件SMTP地址", "web_mail_smtp_host", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_smtp_port = Config("邮件SMTP端口", "web_mail_smtp_port", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_smtp_user = Config("邮件SMTP账号", "web_mail_smtp_user", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_smtp_pass = Config("邮件SMTP密码", "web_mail_smtp_pass", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_smtp_verify = Config("邮件SMTP验证", "web_mail_smtp_verify", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_validation_template = Config("邮件SMTP验证模板", "web_mail_validation_template", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    mail_validation_content = Config("邮件SMTP验证内容", "web_mail_validation_content", "郝明宸的个人博客", "", 0, STATUS_USEFUL)
    # 4 上传配置
    web_system_upload_image_froala_path = Config("froala编辑器图片上传路径", "web_system_upload_image_froala_path",
                                                 "uploads/froala/image/", "", 0, STATUS_USEFUL)
    web_system_upload_video_froala_path = Config("froala编辑器视频上传路径", "web_system_upload_video_froala_path",
                                                 "uploads/froala/video/", "", 0, STATUS_USEFUL)
    web_system_upload_img_path = Config("图片上传路径", "web_system_upload_img_path", "", "", 0, STATUS_USEFUL)
    web_system_upload_avatar_path = Config("用户头像上传路径", "web_system_upload_avatar_path", "", "", 0, STATUS_USEFUL)
    web_system_font_path = Config("字体文件路径", "web_system_font_path", "", "", 0, STATUS_USEFUL)

    # 权限设置
    auth_admin_index = GroupAuthority("后台仪表盘", "", deletable=DELETABLE_NO)
    auth_admin_post = GroupAuthority("后台文章列表", "", deletable=DELETABLE_NO)
    auth_admin_add_post = GroupAuthority("后台写文章", "", deletable=DELETABLE_NO)
    auth_admin_edit_post = GroupAuthority("后台修改文章", "", deletable=DELETABLE_NO)
    auth_admin_draft_post = GroupAuthority("后台草稿列表", "", deletable=DELETABLE_NO)
    auth_admin_delete_post = GroupAuthority("后台删除文章", "", deletable=DELETABLE_NO)
    auth_admin_category = GroupAuthority("后台类别列表", "", deletable=DELETABLE_NO)
    auth_admin_add_category = GroupAuthority("后台增加类别", "", deletable=DELETABLE_NO)
    auth_admin_edit_category = GroupAuthority("后台修改类别", "", deletable=DELETABLE_NO)
    auth_admin_delete_category = GroupAuthority("后台删除类别", "", deletable=DELETABLE_NO)
    auth_admin_user = GroupAuthority("后台用户列表", "", deletable=DELETABLE_NO)
    auth_admin_add_user = GroupAuthority("后台新增用户", "", deletable=DELETABLE_NO)
    auth_admin_edit_user = GroupAuthority("后台修改用户", "", deletable=DELETABLE_NO)
    auth_admin_delete_user = GroupAuthority("后台删除用户", "", deletable=DELETABLE_NO)
    auth_admin_group = GroupAuthority("后台用户组列表", "", deletable=DELETABLE_NO)
    auth_admin_add_group = GroupAuthority("后台新增用户组", "", deletable=DELETABLE_NO)
    auth_admin_edit_group = GroupAuthority("后台修改用户组", "", deletable=DELETABLE_NO)
    auth_admin_delete_group = GroupAuthority("后台删除用户组", "", deletable=DELETABLE_NO)
    auth_admin_status = GroupAuthority("后台状态列表", "", deletable=DELETABLE_NO)
    auth_admin_property = GroupAuthority("后台属性列表", "", deletable=DELETABLE_NO)
    auth_admin_home_config = GroupAuthority("主页配置列表", "", deletable=DELETABLE_NO)
    auth_admin_admin_config = GroupAuthority("后台配置列表", "", deletable=DELETABLE_NO)
    auth_admin_mail_config = GroupAuthority("邮件配置列表", "", deletable=DELETABLE_NO)
    auth_admin_system_config = GroupAuthority("系统配置列表", "", deletable=DELETABLE_NO)

    # 其他配置
    # auth_admin_delete_group = GroupAuthority("后台删除用户组", "", deletable=DELETABLE_NO)
    # auth_admin_delete_group = GroupAuthority("后台删除用户组", "", deletable=DELETABLE_NO)
    # auth_admin_delete_group = GroupAuthority("后台删除用户组", "", deletable=DELETABLE_NO)
    # auth_admin_delete_group = GroupAuthority("后台删除用户组", "", deletable=DELETABLE_NO)

    data_list = [private, public, draft, publish, deleted, useful, useless, supergroup, manager, viper, user, visitor,
                 superuser,
                 web_home_title, web_home_logo_title, web_home_footer_name, web_home_footer_signature,
                 web_home_posts_pages,
                 web_admin_title, web_admin_logo_title, web_admin_post_per_page, web_admin_user_per_page,
                 web_admin_comment_per_page, web_admin_comment_reply_per_page, web_admin_site_copy,
                 web_admin_site_version, mail_smtp_host,
                 mail_smtp_port,
                 mail_smtp_user, mail_smtp_pass, mail_smtp_verify, mail_validation_template,
                 mail_validation_content, web_system_upload_image_froala_path, web_system_upload_video_froala_path,
                 web_system_upload_img_path, web_system_upload_avatar_path, web_system_font_path, auth_admin_index,
                 auth_admin_post,
                 auth_admin_add_post, auth_admin_edit_post, auth_admin_draft_post, auth_admin_delete_post,
                 auth_admin_category,
                 auth_admin_add_category, auth_admin_edit_category, auth_admin_delete_category, auth_admin_user,
                 auth_admin_add_user, auth_admin_edit_user, auth_admin_delete_user, auth_admin_group,
                 auth_admin_add_group,
                 auth_admin_edit_group, auth_admin_delete_group, auth_admin_status, auth_admin_property,
                 auth_admin_home_config,
                 auth_admin_admin_config, auth_admin_mail_config, auth_admin_system_config]

    for x in data_list:
        db.session.add(x)
    db.session.commit()
    print("初始化完成")
