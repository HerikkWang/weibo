import re
import json

def sServerData(serverData):
    p = re.compile('\((.*)\)')
    jsondata = p.search(serverData).group(1)
    data = json.loads(jsondata)
    return data

def sRedirectData(text):
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    loginUrl = p.search(text).group(1)
    print('loginUrl: '+loginUrl)
    return loginUrl