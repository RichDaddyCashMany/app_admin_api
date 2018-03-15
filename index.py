from flask import Flask
from flask_restful import Api
from config.config import Config
import os
from flask_cors import CORS
from util.db import DB
# admin
from resources.admin.user import UserList
from resources.admin.common import ValidImageCreate, QCloudCosSign
from resources.admin.admin import AdminLogin
from resources.admin.notice import NoticeList, NoticeOffline, NoticeAdd
from resources.admin.app import AppVersionSituation, AppVersionSave
from resources.admin.message import MessageBoardList, MessageList, MessageAdd
# user
from resources.app.user import UserLogin, UserReg
from resources.app.notice import SystemLaunch, SystemNotice,SystemBanner
from resources.app.message import UserMessageAdd, UserMessageClose
from resources.app.app import UserAppVersion

# 设置根目录
Config.ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

# 开启cors
CORS(app)

# 初使化SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASSWORD + '@' + \
                                        Config.MYSQL_HOST+ '/' + Config.MYSQL_DBNAME
# 不配置会报错提示。如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 密钥，不配置无法对session字典赋值
app.config['SECRET_KEY'] = os.urandom(24)
# 显示SQLAlchemy的sql语句日志
app.config["SQLALCHEMY_ECHO"] = True

# 缓存全局db对象，每次重新创建会导致事务不是同一个
DB.init(app)

# api
api = Api(app)

# 管理台接口
api.add_resource(ValidImageCreate, '/common/validImage/create')  # 生成图片验证码
api.add_resource(AdminLogin, '/admin/login')  # 管理员登录
api.add_resource(NoticeList, '/notice/list')  # 公告列表
api.add_resource(NoticeOffline, '/notice/offline')  # 公告下线
api.add_resource(NoticeAdd, '/notice/add')  # 公告增加、修改
api.add_resource(QCloudCosSign, '/common/QCloud/sign')  # 腾讯云COS多次签名
api.add_resource(AppVersionSituation, '/app/version/detail')  # app版本信息
api.add_resource(AppVersionSave, '/app/version/save')  # 保存app版本信息
api.add_resource(UserList, '/user/list')  # 用户列表
api.add_resource(MessageBoardList, '/message/list')  # 留言板
api.add_resource(MessageList, '/message/detail')  # 留言详情
api.add_resource(MessageAdd, '/message/add')  # 留言回复
# app接口
api.add_resource(UserLogin, '/api/user/login')  # 用户登录
api.add_resource(UserReg, '/api/user/reg')  # 用户注册
api.add_resource(SystemLaunch, '/api/sys/launch')  # 闪屏
api.add_resource(SystemNotice, '/api/sys/notice')  # 公告
api.add_resource(SystemBanner, '/api/sys/banner')  # banner
api.add_resource(UserMessageAdd, '/api/message/add')  # 留言新增
api.add_resource(UserMessageClose, '/api/message/close')  # 留言关闭
api.add_resource(UserAppVersion, '/api/app/version')  # 版本

if __name__ == '__main__':
    # threaded=True 防止开发服务器阻塞
    app.run(host='0.0.0.0', threaded=True, debug=True)
