from flask_restful import fields, marshal
from util.db import DB
from table.model import AppConfig
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi


class UserAppVersion(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        config = DB.session.query(AppConfig).first()
        dic = {
            'ios_ver': fields.String,
            'ios_force_update': fields.Boolean,
            'ios_update_url': fields.String,
            'ios_update_content': fields.String,
            'ios': fields.Integer(attribute='ios_review'),
            'android_ver': fields.String,
            'android_force_update': fields.Boolean,
            'android_update_url': fields.String,
            'android_update_content': fields.String
        }

        return CommonUtil.json_response(0, '获取成功', marshal(config, dic))
