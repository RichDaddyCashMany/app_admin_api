from flask_restful import reqparse, fields, marshal
from util.db import DB
from util.commonUtil import CommonUtil
from util.checkUtil import CheckUtil
from resources.baseApi import BaseApi
from table.model import MessageBoard, User, MessageBoardMsg
import math
from util.convertUtil import ConvertTimeStamp, ConvertEmptyStr
from util.valid import Valid
import time


# 留言板列表
class MessageBoardList(BaseApi):
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
                boards = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                          User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(User.username.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    order_by(MessageBoard.create_at.desc()). \
                    limit(args.size).offset((args.page - 1) * args.size). \
                    all()
                boards = CommonUtil.sql_result_to_json(boards)
                count = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                         User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(User.username.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    count()
            elif args.searchType == 'nick_name':
                boards = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                          User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(User.nick_name.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    order_by(MessageBoard.create_at.desc()). \
                    limit(args.size).offset((args.page - 1) * args.size). \
                    all()
                boards = CommonUtil.sql_result_to_json(boards)
                count = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                         User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(User.nick_name.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    count()
            elif args.searchType == 'message':
                boards = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                          User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(MessageBoardMsg.message.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    order_by(MessageBoard.create_at.desc()). \
                    limit(args.size).offset((args.page - 1) * args.size). \
                    all()
                boards = CommonUtil.sql_result_to_json(boards)
                count = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                         User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                    join(User, MessageBoardMsg). \
                    filter(MessageBoard.user_id == User.id). \
                    filter(MessageBoardMsg.message.like('%' + args.searchWords + '%')). \
                    filter(MessageBoard.id == MessageBoardMsg.board_id). \
                    count()
            else:
                boards = None
                count = 0
        else:
            boards = DB.session.query(MessageBoard.record_id, MessageBoard.create_at, MessageBoard.close_at,
                                      User.username, User.nick_name, User.avatar, MessageBoardMsg.message). \
                join(User, MessageBoardMsg). \
                filter(MessageBoard.user_id == User.id). \
                filter(MessageBoard.id == MessageBoardMsg.board_id). \
                order_by(MessageBoard.create_at.desc()). \
                limit(args.size).offset((args.page - 1) * args.size). \
                all()
            boards = CommonUtil.sql_result_to_json(boards)
            count = DB.session.query(MessageBoard).count()

        dic = {
            'record_id': fields.String,
            'create_at': ConvertTimeStamp(),
            'close_at': ConvertTimeStamp(),
            'username': fields.String,
            'message': fields.String,
            'avatar': fields.String,
            'nick_name': fields.String
        }

        data = {
            'list': marshal(boards, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)


# 留言列表
class MessageList(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('record_id', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        board = DB.session.query(MessageBoard).\
            filter(MessageBoard.record_id == args.record_id).\
            first()
        if board is None:
            return CommonUtil.json_response(-1, '记录不存在')

        # 用户留言
        user_msgs = DB.session.query(MessageBoardMsg.message_id, MessageBoardMsg.message, MessageBoardMsg.create_at,
                                MessageBoardMsg.is_admin, User.username, User.avatar).\
            join(User). \
            filter(MessageBoardMsg.board_id == board.id).\
            order_by(MessageBoardMsg.create_at.desc()).\
            all()
        user_msgs = CommonUtil.sql_result_to_json(user_msgs)

        # 管理呐留言，因为没有user_id，所以分两次查询
        admin_msgs = DB.session.query(MessageBoardMsg.message_id, MessageBoardMsg.message, MessageBoardMsg.create_at,
                         MessageBoardMsg.is_admin). \
            filter(MessageBoardMsg.is_admin == 1). \
            filter(MessageBoardMsg.board_id == board.id). \
            order_by(MessageBoardMsg.create_at.desc()). \
            all()
        admin_msgs = CommonUtil.sql_result_to_json(admin_msgs)

        msgs = user_msgs + admin_msgs
        # 排序
        msgs = sorted(msgs, key=lambda x: x['create_at'])

        dic = {
            'message_id': fields.String,
            'message': fields.String,
            'create_at': ConvertTimeStamp(),
            'is_admin': fields.Integer,
            'username': ConvertEmptyStr(),
            'avatar': ConvertEmptyStr,
        }

        return CommonUtil.json_response(0, '获取成功', marshal(msgs, dic))


# 留言回复
class MessageAdd(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('record_id', required=True)
        parser.add_argument('message', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.message) is False:
            return CommonUtil.json_response(-1, '回复内容不能为空')

        board = DB.session.query(MessageBoard). \
            filter(MessageBoard.record_id == args.record_id). \
            first()
        if board is None:
            return CommonUtil.json_response(-1, '记录不存在')
        elif board.close_at is not None:
            return CommonUtil.json_response(-1, '已结单不能再回复了')

        msg = MessageBoardMsg(
            board_id=board.id,
            message_id=CommonUtil.md5(str(time.time()) + 'admin'),
            message=args.message,
            create_at=int(time.time()),
            is_admin=True
        )

        DB.session.add(msg)
        DB.session.commit()

        return CommonUtil.json_response(0, '提交成功')
