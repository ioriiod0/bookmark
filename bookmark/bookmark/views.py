#coding=utf-8

from pyramid.view import view_config
from pyramid.response import Response
import logging
import pymongo
import hashlib
import base64
from Crypto.Cipher import ARC4

log = logging.getLogger(__name__)


#
MD5_SALT = "Dd%^2d*^d$&2mm"
REMEMBER_ME_KEY = "HY365sd$%#$2ghf"
#
E_SUCCESS = (0,"OK")
E_EMAIL_ALREADY_REGISTED = (-1,"该邮箱已经注册")
E_BAD_EMAIL = (-2,"错误的邮箱格式")
E_BAD_PASSWORD = (-3,"错误的密码格式")
E_SAVE_DB_FAILED = (-4,"服务器忙，请稍后再试")
E_BAD_DATA_FORMAT = (-5,"数据传输出现问题")
#
E_USER_NOT_FOUND = (-7,"用户名不存在")
E_WRONG_PW = (-8,"密码错误")
#
E_UNKOWN = (-10000,"服务器发生未知错误")
#

def md5(password):
    m = hashlib.md5()
    m.update(password)
    m.update(MD5_SALT)
    return m.hexdigest()

def encrypt(string):
    rc4 = ARC4.new(REMEMBER_ME_KEY)
    temp = rc4.encrypt(string)
    return base64.encodestring(temp);


def decrypt(string):
    rc4 = ARC4.new(REMEMBER_ME_KEY)
    temp = base64.decodestring(string)
    return rc4.decrypt(temp)


@view_config(route_name='register', renderer='json')
def register(request):
    try:
        json_body = request.json_body
        log.debug(json_body)

        email = json_body["email"]
        password = json_body["password"]

        #todo: some verify here.
        password_md5 = md5(password)
        log.debug(password_md5)
        #
        user_collection = request.db.users
        if user_collection.find_one({"account":email,"type":"email"}):
            return {'ret':E_EMAIL_ALREADY_REGISTED[0],'msg':E_EMAIL_ALREADY_REGISTED[1]}

        if not user_collection.insert({"account":email,"password":password_md5,"type":"email"}):
            return {'ret':E_SAVE_DB_FAILED[0],'msg':E_SAVE_DB_FAILED[1]}

        return {'ret':E_SUCCESS[0],'msg':E_SUCCESS[1]}
    except KeyError,e:
        log.debug(e)
        return {'ret':E_BAD_DATA_FORMAT[0],'msg':E_BAD_DATA_FORMAT[1]}
    except Exception,e:
        log.debug(e)
        return {'ret':E_UNKOWN[0],'msg':E_UNKOWN[1]}


@view_config(route_name='login', renderer='json')
def login(request):
    try:
        json_body = request.json_body
        session = request.session
        log.debug(json_body)

        email = json_body["email"]
        password = json_body["password"]
        remember_me = json_body["remember_me"]
        #
        user_collection = request.db.users
        user = user_collection.find_one({"account":email,"type":"email"})
        if not user:
            return {'ret':E_USER_NOT_FOUND[0],'msg':E_USER_NOT_FOUND[1]}

        password_md5 = md5(password)
        log.debug(password_md5)

        if user["password"] != password_md5:
            return {'ret':E_WRONG_PW[0],'msg':E_WRONG_PW[1]}

        if remember_me:
            response = request.response
            response.set_cookie('remember_me', encrypt("%s,%s" % (email,"email")) )

        session["user"] = email
        session["type"] = "email"

        return {'ret':E_SUCCESS[0],'msg':E_SUCCESS[1]}

    except KeyError,e:
        log.debug(e)
        return {'ret':E_BAD_DATA_FORMAT[0],'msg':E_BAD_DATA_FORMAT[1]}
    except Exception,e:
        log.debug(e)
        return {'ret':E_UNKOWN[0],'msg':E_UNKOWN[1]}


# @view_config(route_name='bookmark_add', renderer='json')
# def bookmark_add(request):
#     log.debug("bookmark_add start")
#     if hasattr(request,"json_body") and request.json_body:
#         bookmarks = request.db.bookmarks
#         return {'ret':0,'msg':'ok'}
#     else :
#         return {'ret':-1,'msg':'failed'}


# @view_config(route_name='bookmark_del', renderer='json')
# def bookmark_delete(request):
#     log.debug("bookmark_delete start")
#     if hasattr(request,"json_body") and request.json_body:
#         body = request.body
#         return {'ret':0,'msg':'ok'}
#     else :
#         return {'ret':-1,'msg':'failed'}



# @view_config(route_name='bookmark_search', renderer='json')
# def bookmark_search(request):
#     log.debug("bookmark_search start")
#     if hasattr(request,"json_body") and request.json_body:
#         body = request.body
#         return {'ret':0,'msg':'ok',"bookmarks":[]}
#     else :
#         return {'ret':-1,'msg':'failed'}


