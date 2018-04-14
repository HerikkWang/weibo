import time
from selenium import webdriver
import csv
import re

# 获取答主微博认证，粉丝数，标签信息
chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath) # 构建浏览器
wd.set_page_load_timeout(30)
loginUrl = 'http://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='

wd.get(loginUrl) # 进入登陆界面
# wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('13777015316') # 输入用户名
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('595432157') # 输入密码
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click() # 点击登陆
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(input("输入验证码： "))
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()#再次点击登陆

time.sleep(20) # 等待20秒用于输入用户名，密码并登录

csv_read_path = r'C:\Users\Administrator\PycharmProjects\weibo\weibo_data_2_1_processed.csv'
csv_write_path = r"C:\Users\Administrator\PycharmProjects\weibo\weibo_data_3_1.csv"

data = [['replier_fans_num', 'replier_authentication', 'replier_tags']]
t = 0  # 计数器
with open(csv_read_path, 'r+', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        replier_id = row['replier_id']
        fans_num_url = 'http://weibo.cn/%s'%replier_id  # 用于获取用户粉丝，关注数量的url
        tag_url = 'http://weibo.cn/account/privacy/tags/?uid=%s'%replier_id  # 用于获取用户标签信息的url
        info_url = 'http://weibo.cn/%s/info'%replier_id  # 用于获取用户微博认证信息的url
        replier_fans_num = ''
        tags_info = []
        replier_authentication = ''

        try:  # 获取用户粉丝数量
            wd.get(fans_num_url)
            text_1 = wd.find_element_by_class_name('tip2').text
            replier_fans_num = re.findall(".*粉丝\[(.*)\]\s分组.*", text_1)[0]
        except:
            pass

        try:  # 获取用户标签信息
            wd.get(tag_url)
            try:  # 只有一个标签的情况下，尝试采集
                tag = wd.find_element_by_xpath('/html/body/div[6]/a').text
                tags_info.append(tag)
            except:
                pass

            # 有多个标签的情况下，尝试采集，最大采集数量设置为15
            n = 2
            while n <= 15:
                try:
                    tags = wd.find_element_by_xpath('/html/body/div[6]/a[%d]'%n).text
                    tags_info.append(tags)
                    n = n+1
                except:
                    n = n+1
        except:
            pass

        try:  # 采集用户微博认证信息
            wd.get(info_url)
            authentication_info = wd.find_element_by_xpath('/html/body/div[6]').text
            if authentication_info.split('\n')[1].startswith('认证'):
                replier_authentication = authentication_info.split('\n')[1][3:]
        except:
            pass
        time.sleep(4)  # 防止频繁访问引起的访问拒绝
        t = t+1
        print(str(t)+': '+str([replier_fans_num, replier_authentication, tags_info]))
        data.append([replier_fans_num, replier_authentication, tags_info])

with open(csv_write_path, 'w+', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)









