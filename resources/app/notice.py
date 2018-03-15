from flask_restful import fields, marshal
from util.db import DB
from table.model import Notice, MessageBoard, MessageBoardMsg
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
import time


def get_luanch_notice(notice_type):
    now = int(time.time())
    # 已经开始 还未结束 上线中
    notice = DB.session.query(Notice).filter(Notice.type == notice_type).filter(Notice.begin_time < now). \
        filter(Notice.end_time > now).filter(Notice.enable == 1).first()

    if notice is None:
        return CommonUtil.json_response(-1, '获取失败')

    dic = {
        'record_id': fields.String,
        'title': fields.String,
        'content': fields.String,
        'picture_url': fields.String,
        'url': fields.String
    }

    return CommonUtil.json_response(0, '获取成功', marshal(notice, dic))


# 启动页
class SystemLaunch(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        return get_luanch_notice(0)


# 公告
class SystemNotice(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        return get_luanch_notice(1)


# banner
class SystemBanner(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        now = int(time.time())
        # 已经开始 还未结束 上线中
        notice = DB.session.query(Notice).filter(Notice.type == 2).filter(Notice.begin_time < now). \
            filter(Notice.end_time > now).filter(Notice.enable == 1).all()

        if notice is None:
            return CommonUtil.json_response(0, '获取成功', [])

        dic = {
            'record_id': fields.String,
            'remark': fields.String,
            'picture_url': fields.String,
            'url': fields.String
        }

        return CommonUtil.json_response(0, '获取成功', {"list": marshal(notice, dic)})


