# -*- coding: utf-8 -*-
import weiboLogin
import Login
import urllib.request
import re
import sys


#调用模拟登录的程序，从网页中抓取指定URL的数据，获取原始的HTML信息存入raw_html.txt中
def get_rawHTML(url):
    #Login.login()
    content = urllib.request.urlopen(url).read().decode('utf-8')
    fp_raw = open("example_page.txt","w+")
    fp_raw.write(content)
    fp_raw.close()                # 获取原始的HTML写入文件
    # print "成功爬取指定网页源文件并且存入raw_html.txt"
    return content   # 返回值为原始的HTML文件内容

if __name__ == '__main__':
    Login.login()   #先调用登录函数
    #url = 'http://weibo.com/yaochen?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1#feedtop'   #姚晨
    url = 'https://weibo.cn/1961640291/info'   #自行设定要抓取的网页
    get_rawHTML(url)