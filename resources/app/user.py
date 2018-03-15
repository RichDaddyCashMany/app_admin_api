from flask_restful import reqparse, fields, marshal
from util.db import DB
from table.model import User
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
import time


# 用户注册
class UserReg(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user = DB.session.query(User).filter(User.username == args.username).first()
        if user is None:

            now = int(time.time())

            user = User(
                user_id=CommonUtil.md5(now),
                username=args.username,
                password=CommonUtil.create_user_password(args.username, args.password)
            )
            DB.session.add(user)
            DB.session.commit()

            return CommonUtil.json_response(0, '注册成功')
        else:
            return CommonUtil.json_response(-1, '用户已存在')


# 用户登录
class UserLogin(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user = DB.session.query(User).filter(User.username == args.username).first()
        if user is None:
            return CommonUtil.json_response(-1, "用户不存在")

        if user.password == CommonUtil.create_user_password(args.username, args.password):
            # 生成新token
            user.token = CommonUtil.create_user_token(args.username)
            DB.session.commit()

            user = DB.session.query(User).filter(User.username == args.username).first()
            dic = {
                'token': fields.String,
                'user_id': fields.String,
                'username': fields.String,
                'phone': fields.String,
                'email': fields.String,
                'expire_at': fields.String,
                'last_login_ip': fields.String,
                'last_login_time': fields.String,
                'real_name': fields.String,
                'id_card': fields.String,
                'address': fields.String,
                'create_at': fields.String,
                'nike_name': fields.String,
                'is_identity': fields.String,
                'avatar': fields.String,
                'sex': fields.String
            }

            return CommonUtil.json_response(0, "登录成功", marshal(user, dic))
        else:
            return CommonUtil.json_response(-1, "密码错误")
