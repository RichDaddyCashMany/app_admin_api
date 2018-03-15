from util.db import DB
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from table.model import AppConfig
from flask_restful import fields, marshal, reqparse
from util.checkUtil import CheckUtil
from util.valid import Valid


# app版本配置情况
class AppVersionSituation(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        config = DB.session.query(AppConfig).first()
        dic = {
            'ios_ver': fields.String,
            'ios_force_update': fields.String,
            'ios_update_url': fields.String,
            'ios_update_content': fields.String,
            'ios_review': fields.String,
            'android_ver': fields.String,
            'android_force_update': fields.String,
            'android_update_url': fields.String,
            'android_update_content': fields.String
        }

        return CommonUtil.json_response(0, '获取成功', marshal(config, dic))


# 保存app版本配置
class AppVersionSave(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('ios_ver', required=True)
        parser.add_argument('ios_force_update')
        parser.add_argument('ios_update_url')
        parser.add_argument('ios_update_content')
        parser.add_argument('ios_review')
        parser.add_argument('android_ver', required=True)
        parser.add_argument('android_force_update')
        parser.add_argument('android_update_url')
        parser.add_argument('android_update_content')
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.ios_ver) is False or Valid.is_non_empty_str(args.android_ver) is False:
            return CommonUtil.json_response(-1, '版本号必填')

        config = DB.session.query(AppConfig).first()
        if config is None:
            DB.session.add(AppConfig())
            DB.session.commit()
            config = DB.session.query(AppConfig).first()

        config.ios_ver = args.ios_ver
        config.ios_force_update = args.ios_force_update
        config.ios_update_url = args.ios_update_url
        config.ios_update_content = args.ios_update_content
        config.ios_review = args.ios_review
        config.android_ver = args.android_ver
        config.android_force_update = args.android_force_update
        config.android_update_url = args.android_update_url
        config.android_update_content = args.android_update_content
        DB.session.commit()

        return CommonUtil.json_response(0, '保存成功')