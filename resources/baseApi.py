from flask_restful import Resource, reqparse
from flask import request, session
import json
import os
import hashlib
from util.log import Logger


# 这个是Api基类，可以做统一处理
class BaseApi(Resource):
    def __init__(self):
        md5 = hashlib.md5()
        md5.update(os.urandom(24))
        session['requestId'] = md5.hexdigest()

        Logger.log("请求 请求id：%s\n来源IP：%s\n请求方法：%s\n请求路径：%s\n请求参数：%s" % (session['requestId'], request.environ['REMOTE_ADDR'], request.environ['REQUEST_METHOD'], request.url, json.dumps(request.form)))
        Resource.__init__(self)

