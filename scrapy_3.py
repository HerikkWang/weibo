import time
from selenium import webdriver
import re
import pymysql

# 连接mysql
csv_read_path = 'weibo_new_page_url.csv'
conn = pymysql.connect(host='localhost', user='root', password='herik', database='weibodata', charset='utf8mb4')
cur = conn.cursor()
cur.execute('use weibodata')


# 获取答主微博认证，粉丝数，标签信息
chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath) # 构建浏览器
wd.set_page_load_timeout(30)
loginUrl = 'http://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='

wd.get(loginUrl)  # 进入登陆界面
# wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('13777015316') # 输入用户名
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('595432157') # 输入密码
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click() # 点击登陆
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(input("输入验证码： "))
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()#再次点击登陆

time.sleep(20)  # 等待20秒用于输入用户名，密码并登录

cur.execute('select replier_id, page_url from weibo_scrapy_1')
tup = cur.fetchall()

t = 0  # 计数器
while t < len(tup):
    page_url = tup[t][1][1:-1]
    replier_id = tup[t][0][1:-1]  # 从数据库中取出的字符串带有''
    fans_num_url = 'http://weibo.cn/%s' % replier_id  # 用于获取用户粉丝，关注数量的url
    tag_url = 'http://weibo.cn/account/privacy/tags/?uid=%s' % replier_id  # 用于获取用户标签信息的url
    info_url = 'http://weibo.cn/%s/info' % replier_id  # 用于获取用户微博认证信息的url
    replier_fans_num = '0'
    tags_info = ''
    replier_authentication = ''

    try:  # 获取用户粉丝数量
        wd.get(fans_num_url)
        text_1 = wd.find_element_by_class_name('tip2').text
        replier_fans_num = re.findall(".*粉丝\[(.*)\]\s分组.*", text_1)[0]
    except Exception:
        pass

    try:  # 获取用户标签信息
        wd.get(tag_url)
        try:  # 只有一个标签的情况下，尝试采集
            tag = wd.find_element_by_xpath('/html/body/div[6]/a').text
            tags_info += tag
        except Exception:
            pass

        # 有多个标签的情况下，尝试采集，最大采集数量设置为15
        n = 2
        while n <= 15:
            try:
                tags = wd.find_element_by_xpath('/html/body/div[6]/a[%d]'%n).text
                tags_info = tags_info + ' ' + tags
                n = n+1
            except Exception:
                n = n+1
    except Exception:
        pass

    try:  # 采集用户微博认证信息
        wd.get(info_url)
        authentication_info = wd.find_element_by_xpath('/html/body/div[6]').text
        if authentication_info.split('\n')[1].startswith('认证'):
            replier_authentication = authentication_info.split('\n')[1][3:]
    except Exception:
        pass
    time.sleep(4)  # 防止频繁访问引起的访问拒绝
    t = t+1
    print(str(t)+': '+str([replier_fans_num, replier_authentication, tags_info]))
    cur.execute("insert into weibo_scrapy_3 (page_url, replier_fans_num, replier_authentication, tags_info) values"
                "(\"%s\", %s, \"%s\", \"%s\")", (page_url, replier_fans_num, replier_authentication, tags_info))
    cur.connection.commit()


cur.close()
conn.close()
wd.close()
