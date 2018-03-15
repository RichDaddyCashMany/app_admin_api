"""
这里封装了一些常用的方法
"""
from flask import session
import json
from util.log import Logger
import hashlib
import time


class CommonUtil:
    # 返回json数据
    @classmethod
    def json_response(cls, code, msg, data={}):
        res = {
            "code": code,
            "message": msg,
            "data": data
        }
        Logger.log("响应 请求id：%s\n返回内容：%s" % (session['requestId'], json.dumps(res)))
        return res

    # python3.6比如md5经常提示参数类型不对
    @classmethod
    def utf8str(cls, arg):
        ret = "{}".format(arg).encode('utf-8').decode()
        if ret != "{}":
            return ret
        else:
            raise AssertionError('convert {} to utf-8 error'.format(arg))

    # md5
    @classmethod
    def md5(cls, arg):
        obj = hashlib.md5()
        obj.update(cls.utf8str(arg).encode('utf-8'))
        return obj.hexdigest()

    # 创建管理员token
    @classmethod
    def create_admin_token(cls, value):
        return cls.md5('admin_'+ value + str(time.time()))

    # 创建用户token
    @classmethod
    def create_user_token(cls, value):
        return cls.md5('user_' + value + str(time.time()))

    # 用户密码，传进来的username已经是md5
    @classmethod
    def create_user_password(cls, username, password):
        return cls.md5(username + password + '_pwd')

    # 时间戳转时间
    @classmethod
    def timestamp_to_time(cls, value):
        time_local = time.localtime(value)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        if time_str:
            return time_str
        else:
            return ''

    # 时间转时间戳
    @classmethod
    def time_to_timestamp(cls, value, formatter="%Y-%m-%d %H:%M:%S"):
        time_local = time.strptime(value, formatter)
        return int(time.mktime(time_local))

    # sqlalchemy复合查询结果是result对象，不能用marshal转换，所以提前转成字典或数组
    @classmethod
    def sql_result_to_json(cls, result):
        if type(result) is dict:
            return result._asdict()
        else:
            arr = []
            for item in result:
                arr.append(item._asdict())
            return arr
