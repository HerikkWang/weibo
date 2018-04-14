import urllib.request
import urllib.parse
import http.cookiejar
import WeiboSearch
import time
import json
import re
import cv2
import numpy as np
import rsa
import binascii
import base64

class WeiboLogin:
    def __init__(self, user, pwd, enableProxy=False):
        print('初始化新浪微博登录...')
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy

        self.postHeader = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"}
        self.loginUrl = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.login_url_1 = 'https://passport.weibo.com/wbsso/login'

    def EnableCookie(self, enableProxy):
        cookiejar = http.cookiejar.CookieJar()
        cookie = urllib.request.HTTPCookieProcessor(cookiejar)
        opener = urllib.request.build_opener(cookie)
        urllib.request.install_opener(opener)

    def GetServerTime(self):
        print('getting server time and nonce...')
        encodedUserName = self.GetUserName(self.userName)
        serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=%s"%(encodedUserName,str(int(time.time() * 1000)))
        serverData = urllib.request.urlopen(serverUrl).read().decode('utf-8')
        print(serverData)
        # urlopen方法返回的是bytes对象，通过decode('utf-8')将bytes对象转换为str
        try:
            serverdata = WeiboSearch.sServerData(serverData)
            print('Get servertime sucessfully!')
            return serverdata
        except:
            print('解析serverdata出错！')
            return None

    def getData(self,url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content

    def GetUserName(self,userName):
        userNameTemp = urllib.request.quote(userName)
        userNameEncoded = base64.b64encode(userNameTemp.encode('utf-8'))
        return userNameEncoded.decode('utf-8')

    def get_pwd(self,password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, int('10001', 16))
        message = (str(servertime) + '\t' + str(nonce) + '\n' + str(password)).encode('utf-8')
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        return passwd.decode()

    def get_raw_html(self,url):
        content = urllib.request.urlopen(url).read().decode('utf-8')
        raw_file = open('main_html.txt', 'w+', encoding='utf-8')
        raw_file.write(content)
        raw_file.close()
        return content

    def Login(self):
        self.EnableCookie(self.enableProxy)
        serverdata = self.GetServerTime()
        serverTime = str(serverdata['servertime'])
        nonce = serverdata['nonce']
        pubkey = serverdata['pubkey']
        rsakv = serverdata['rsakv']
        encodedUserName = self.GetUserName(self.userName)
        encodedPassWord = self.get_pwd(self.passWord, serverTime, nonce, pubkey)
        postData = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": rsakv,
            "servertime": serverTime,
            "nonce": nonce,
            "su": encodedUserName,
            "sp": encodedPassWord,
            "returntype": "TEXT",
        }
        try:
            if serverdata['showpin'] == 1:
                url_pincheck = 'http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s'%(int(time.time()),serverdata['pcid'])
                resp = urllib.request.urlopen(url_pincheck)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                cv2.imshow("Image", image)
                cv2.waitKey(0)
                code = input('请输入验证码：')
                postData['pcid'] = serverdata['pcid']
                postData['door'] = code
        except KeyError:
            print('无需输入验证码')

        postData = urllib.parse.urlencode(postData)
        postData = postData.encode('utf-8')
        print('Get postdata successfully!')
        req = urllib.request.Request(self.loginUrl, postData, self.postHeader)
        result = urllib.request.urlopen(req)
        text = result.read()
        print(text)

        json_data_1 = json.loads(text.decode('utf-8'))
        if json_data_1['retcode'] == '0':
            print('预登录成功！')
            params = {
                'callback': 'sinaSSOController.callbackLoginStatus',
                'client': 'ssologin.js(v1.4.19)',
                'ticket': json_data_1['ticket'],
                'ssosavestate': int(time.time()),
                '_': int(time.time()*1000),
            }
            params = urllib.parse.urlencode(params).encode('utf-8')
            response = urllib.request.Request(self.login_url_1, params, self.postHeader)
            result_2 = urllib.request.urlopen(response)
            text_2 = result_2.read().decode('utf-8')
            json_data_2 = json.loads(re.search(r'\((?P<result>.*)\)',text_2).group('result'))
            if json_data_2['result'] is True:
                user_uniqueid = json_data_2['userinfo']['uniqueid']
                user_nick = json_data_2['userinfo']['displayname']
        if user_nick and user_uniqueid:
            print('user id: '+user_uniqueid, 'user name: '+user_nick)
            return True
        else:
            return False
