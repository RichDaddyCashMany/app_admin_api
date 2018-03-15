from flask_restful import reqparse, fields, marshal
from util.db import DB
from table.model import Admin
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.checkUtil import CheckUtil


# 管理员登录
class AdminLogin(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('validId', required=True)
        parser.add_argument('validValue', required=True)
        args = parser.parse_args()

        # 效验验证码
        result = CheckUtil.check_valid_image(args.validId, args.validValue)
        if result.code != 0:
            CommonUtil.json_response(result.code, result.message)

        admin = DB.session.query(Admin).filter(Admin.username == args.username).first()
        if admin is None:
            return CommonUtil.json_response(-1, "账号不存在")

        if admin.password == args.password:
            # 生成新token
            admin.token = CommonUtil.create_admin_token(args.username)
            DB.session.commit()

            admin = DB.session.query(Admin).filter(Admin.username == args.username).first()
            dic = {
                'token': fields.String
            }

            return CommonUtil.json_response(0, "登录成功", marshal(admin, dic))
        else:
            return CommonUtil.json_response(-1, "密码错误")
