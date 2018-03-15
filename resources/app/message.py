from flask_restful import reqparse
from util.db import DB
from table.model import MessageBoard, MessageBoardMsg
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
import time
from util.valid import Valid
from util.checkUtil import CheckUtil
import jpush
import sys
import os


# 留言
class UserMessageAdd(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('record_id')  # 如果是新增record_id传空
        parser.add_argument('message', required=True, type=str)
        args = parser.parse_args()

        # 效验token
        res = CheckUtil.check_user_token(args.token)
        if res.code != 0:
            return CommonUtil.json_response(res.code, res.message)
        user = res.data

        if Valid.is_non_empty_str(args.message) is False:
            return CommonUtil.json_response(-1, '内容不能为空')

        if Valid.is_non_empty_str(args.record_id) is False:
            board = MessageBoard(
                record_id=CommonUtil.md5(str(time.time()) + 'msg_board' + args.token),
                create_at=int(time.time()),
                user_id=user.id
            )
            DB.session.add(board)
            DB.session.commit()
        else:
            board = DB.session.query(MessageBoard).filter(MessageBoard.record_id == args.record_id).first()
            if board is None:
                return CommonUtil.json_response(-1, '留言记录不存在')

        msg = MessageBoardMsg(
            board_id=board.id,
            message_id=CommonUtil.md5(str(time.time()) + 'msg' + args.token),
            user_id=user.id,
            message=args.message,
            create_at=int(time.time()),
            is_admin=False
        )

        DB.session.add(msg)
        DB.session.commit()

        return CommonUtil.json_response(0, '留言成功')


# 关闭留言
class UserMessageClose(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('record_id')
        args = parser.parse_args()

        # 效验token
        res = CheckUtil.check_user_token(args.token)
        if res.code != 0:
            return CommonUtil.json_response(res.code, res.message)

        board = DB.session.query(MessageBoard).filter(MessageBoard.record_id == args.record_id).first()
        if board is None:
            return CommonUtil.json_response(-1, '留言记录不存在')

        board.close_at = int(time.time())
        DB.session.commit()

        return CommonUtil.json_response(0, '关闭成功')



