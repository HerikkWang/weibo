import urllib.parse
import urllib.request
import base64
import rsa
import binascii

def PostEncode(userName, passWord, serverTime, nonce, pubkey, rsakv):
    encodedUserName = GetUserName(userName)
    encodedPassWord = get_pwd(passWord, serverTime, nonce, pubkey)
    postData = {
        "entry": "weibo",
        "gateway": "1",
        "from": "",
        "savestate": "7",
        "userticket": "1",
        'ssosimplelogin':'1',
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
    postData = urllib.parse.urlencode(postData)
    return postData.encode('utf-8')
    # 用于weibologin中post方法的postdata必须为bytes格式，通过encode('utf-8')方法将str转换为bytes


def GetUserName(userName):
    userNameTemp = urllib.request.quote(userName)
    userNameEncoded = base64.b64encode(userNameTemp.encode('utf-8'))
    return userNameEncoded.decode('utf-8')


def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, int('10001',16))
    message = (str(servertime) + '\t' + str(nonce) + '\n' + str(password)).encode('utf-8')
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd.decode()
