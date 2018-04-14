import weiboLogin
import urllib.request
import re

def login():
    username = '13777015316'
    pwd = '595432157'
    weibologin_herik = weiboLogin.WeiboLogin(username, pwd)
    if weibologin_herik.Login():
        print('登录成功!')
