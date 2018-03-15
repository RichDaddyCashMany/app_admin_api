from flask_restful import reqparse, fields, marshal
from util.db import DB
from util.commonUtil import CommonUtil
from util.checkUtil import CheckUtil
from resources.baseApi import BaseApi
from table.model import User
import math
from util.convertUtil import ConvertTimeStamp
from util.valid import Valid


# 用户列表
class UserList(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('page', type=int, required=True)
        parser.add_argument('size', type=int, required=True)
        parser.add_argument('searchType')
        parser.add_argument('searchWords')
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.searchType) and Valid.is_non_empty_str(args.searchWords):
            if args.searchType == 'username':
                users = DB.session.query(User).\
                    filter(User.username.like('%' + args.searchWords + '%')).\
                    order_by(User.create_at.desc()).\
                    limit(args.size).offset((args.page - 1) * args.size).\
                    all()
                count = DB.session.query(User).\
                    filter(User.username.like('%' + args.searchWords + '%')).\
                    count()
            elif args.searchType == 'nick_name':
                users = DB.session.query(User).\
                    filter(User.nick_name.like('%' + args.searchWords + '%')).\
                    order_by(User.create_at.desc()).\
                    limit(args.size).offset((args.page - 1) * args.size).\
                    all()
                count = DB.session.query(User).\
                    filter(User.nick_name.like('%' + args.searchWords + '%')).\
                    count()
            elif args.searchType == 'phone':
                users = DB.session.query(User).\
                    filter(User.phone.like('%' + args.searchWords + '%')).\
                    order_by(User.create_at.desc()).\
                    limit(args.size).offset((args.page - 1) * args.size).\
                    all()
                count = DB.session.query(User).\
                    filter(User.phone.like('%' + args.searchWords + '%')).\
                    count()
            elif args.searchType == 'email':
                users = DB.session.query(User).\
                    filter(User.email.like('%' + args.searchWords + '%')).\
                    order_by(User.create_at.desc()).\
                    limit(args.size).offset((args.page - 1) * args.size).\
                    all()
                count = DB.session.query(User).\
                    filter(User.email.like('%' + args.searchWords + '%')).\
                    count()
            else:
                users = None
                count = 0
        else:
            users = DB.session.query(User).\
                order_by(User.create_at.desc()).\
                limit(args.size).offset((args.page - 1) * args.size).\
                all()
            count = DB.session.query(User).count()

        dic = {
            'user_id': fields.String,
            'username': fields.String,
            'phone': fields.String,
            'email': fields.String,
            'expire_at': ConvertTimeStamp(),
            'last_login_ip': fields.String,
            'last_login_time': ConvertTimeStamp(),
            'real_name': fields.String,
            'id_card': fields.String,
            'address': fields.String,
            'create_at': ConvertTimeStamp(),
            'create_ip': fields.String,
            'nick_name': fields.String,
            'is_identity': fields.String,
            'avatar': fields.String,
            'sex': fields.String
        }

        data = {
            'list': marshal(users, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)
