>* app_admin的接口项目
>* 基于python3.6
>* 使用flask sqlalchemy redis

* 配置

```
config/config.py
```

* 运行

```
// 使用virtualenv创建python3.6的环境目录
// 进入virtualenv环境

// 安装依赖
pip install -r requirements
```

* 部署

[centos7+python3.6+flask+virtualenv+uwsgi+nginx（多站点部署）](https://www.jianshu.com/p/30f422539993)


```
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
```