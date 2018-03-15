from flask_restful import reqparse, fields, marshal
from table.model import Notice
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.checkUtil import CheckUtil
from util.convertUtil import ConvertTimeStamp
import math
from util.valid import Valid
import time
from util.db import DB


# 公告列表
class NoticeList(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('type', required=True)
        parser.add_argument('page', type=int, required=True)
        parser.add_argument('size', type=int, required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        notices = DB.session.query(Notice).filter(Notice.type == args.type).order_by(Notice.create_at.desc())\
            .limit(args.size).offset((args.page - 1) * args.size).all()
        count = DB.session.query(Notice).filter(Notice.type == args.type).count()

        dic = {
            'title': fields.String,
            'content': fields.String,
            'create_at': ConvertTimeStamp(),
            'type': fields.Integer,
            'update_at': ConvertTimeStamp(),
            'record_id': fields.String,
            'picture_url': fields.String,
            'begin_time': ConvertTimeStamp,
            'end_time': ConvertTimeStamp,
            'enable': fields.Integer,
            'url': fields.String,
            'remark': fields.String
        }

        data = {
            'list': marshal(notices, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)


# 下线公告
class NoticeOffline(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('record_id', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        notice = DB.session.query(Notice).filter(Notice.record_id == args.record_id).first()
        if notice.enable is False:
            return CommonUtil.json_response(-1, '已经是下线状态')
        else:
            notice.enable = False
            DB.session.commit()

            return CommonUtil.json_response(0, '操作成功')


# 新增、修改公告
class NoticeAdd(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('type', required=True, type=int)  # 0闪屏 1公告 2banner
        parser.add_argument('style', required=True, type=int)  # 0文字公告 1图片公告
        parser.add_argument('beginTime', required=True, dest='begin_time')
        parser.add_argument('endTime', required=True, dest='end_time')
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('pic', type=str)
        parser.add_argument('record_id', type=str)
        parser.add_argument('remark', type=str)
        parser.add_argument('url', type=str)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_admin_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if args.style == 0:
            if Valid.is_non_empty_str(args.title) is False or Valid.is_non_empty_str(args.content) is False:
                return CommonUtil.json_response(-1, '标题内容不能为空')
        elif Valid.is_non_empty_str(args.pic) is False:
            return CommonUtil.json_response(-1, '图片不能为空')

        begin_time = CommonUtil.time_to_timestamp(args.begin_time)
        end_time = CommonUtil.time_to_timestamp(args.end_time)

        if begin_time >= end_time:
            return CommonUtil.json_response(-1, '开始时间必须小于结束时间')

        if Valid.is_non_empty_str(args.record_id):  # 修改
            notice = DB.session.query(Notice).filter(Notice.record_id == args.record_id).filter(Notice.type == args.type).first()
            if notice is None:
                return CommonUtil.json_response(-1, '记录不存在')
            elif notice.enable is False:
                return CommonUtil.json_response(-1, '已下线不能编辑')
            elif notice.end_time < time.time():
                return CommonUtil.json_response(-1, '已过期不能编辑')

            notice.title = args.title
            notice.content = args.content
            notice.picture_url = args.pic
            notice.url = args.url
            notice.remark = args.remark
            notice.update_at = int(time.time())
            DB.session.commit()

            return CommonUtil.json_response(0, '修改成功')
        else:  # 新增
            # 闪屏、公告同一时段只能有一个
            if args.type == 0 or args.type == 1:
                is_exist = DB.session.query(Notice).filter(Notice.type == args.type).\
                    filter(begin_time <= Notice.end_time).filter(Notice.enable == 1).first()
                if is_exist:
                    return CommonUtil.json_response(-1, '该时段内还有未下线的闪屏公告')

            now = int(time.time())

            notice = Notice(
                type=args.type,
                title=args.title,
                content=args.content,
                picture_url=args.pic,
                url=args.url,
                begin_time=begin_time,
                end_time=end_time,
                remark=args.remark,
                create_at=now,
                update_at=now,
                record_id=CommonUtil.md5(now),
                enable=True
            )
            DB.session.add(notice)
            DB.session.commit()

            return CommonUtil.json_response(0, '新增成功')
