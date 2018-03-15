from flask_restful import fields
from util.commonUtil import CommonUtil


# 时间戳转时间，用于marshal函数，过滤返回字典
class ConvertTimeStamp(fields.Raw):
    def format(self, value):
        ret = CommonUtil.timestamp_to_time(value)
        if ret is None:
            return ''
        else:
            return ret


# None转换成空字符串
class ConvertEmptyStr(fields.Raw):
    def format(self, value):
        if value is None:
            return ''
        else:
            return value
