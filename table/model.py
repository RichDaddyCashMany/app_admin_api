from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 管理员表
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    token = db.Column(db.String(32))


# 公告表
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.String(32), unique=True)
    create_at = db.Column(db.Integer)
    update_at = db.Column(db.Integer)
    type = db.Column(db.Integer)
    title = db.Column(db.String(20))
    content = db.Column(db.Text)
    picture_url = db.Column(db.Text)
    begin_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    enable = db.Column(db.Boolean)
    url = db.Column(db.Text)
    remark = db.Column(db.Text)


# app配置表
class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ios_ver = db.Column(db.String(20))
    ios_force_update = db.Column(db.Integer, default=0)
    ios_update_url = db.Column(db.Text)
    ios_update_content = db.Column(db.Text)
    ios_review = db.Column(db.Integer, default=0)
    android_ver = db.Column(db.String(20))
    android_force_update = db.Column(db.Integer, default=0)
    android_update_url = db.Column(db.Text)
    android_update_content = db.Column(db.Text)


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(100))
    token = db.Column(db.String(32))
    expire_at = db.Column(db.String(11))
    last_login_ip = db.Column(db.String(15))
    last_login_time = db.Column(db.Integer)
    real_name = db.Column(db.String(4))
    id_card = db.Column(db.String(18))
    address = db.Column(db.String(200))
    create_at = db.Column(db.Integer)
    create_ip = db.Column(db.String(15))
    nick_name = db.Column(db.String(10))
    is_identity = db.Column(db.Boolean)
    avatar = db.Column(db.String(200))
    sex = db.Column(db.Boolean)
    msgs = db.relationship('MessageBoardMsg', backref='user')


# 留言板表
class MessageBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.String(32))
    create_at = db.Column(db.Integer)
    close_at = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msgs = db.relationship('MessageBoardMsg', backref='message_board')


# 留言内容
class MessageBoardMsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('message_board.id'), nullable=False)
    message_id = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(1000))
    create_at = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

