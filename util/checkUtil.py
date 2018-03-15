from util.redis import Redis
from util.db import DB
from table.model import Admin, User
from model.response import Response


class CheckUtil:
    # 效验图片验证码
    @classmethod
    def check_valid_image(cls, valid_id, valid_value):
        code = Redis.get(valid_id)

        if code is None:
            return Response(-1, '验证码不存在')
        elif code != valid_value:
            return Response(-1, '验证码错误')
        else:
            Redis.delete(valid_id)
            return Response()

    # 效验token
    @classmethod
    def check_admin_token(cls, token):
        if token is None:
            return Response(1001, '身份信息不存在')
        else:
            admin = DB.session.query(Admin).filter(Admin.token == token).first()
            if admin is None:
                return Response(1001, '账号不存在')
            elif admin.token != token:
                return Response(1001, '身份信息已过期')
            else:
                return Response(0, '', admin)

    # 效验token
    @classmethod
    def check_user_token(cls, token):
        if token is None:
            return Response(1001, '身份信息不存在，请重新登录')
        else:
            user = DB.session.query(User).filter(User.token == token).first()
            if user is None:
                return Response(1001, '账号不存在')
            elif user.token != token:
                return Response(1001, '身份信息已过期，请重新登录')
            else:
                return Response(0, '', user)
