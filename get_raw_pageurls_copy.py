import time
from selenium import webdriver
import csv
import random

chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath) # 构建浏览器
wd.set_page_load_timeout(30)
loginUrl = 'http://www.weibo.com/login.php'

wd.get(loginUrl) # 进入登陆界面
time.sleep(5)
wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('17326089891') # 输入用户名
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('urtheone1') # 输入密码
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click() # 点击登陆
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(input("输入验证码： "))
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()#再次点击登陆

time.sleep(20) # 等待20秒用于输入用户名，密码并登录

# url_part_1 = 'http://s.weibo.com/weibo/%25E6%2588%2591%25E5%259B%25B4%25E8%25A7%2582%25E4%25BA%2586&b=1&nodup=1'
# 搜索‘我围观了’的微博结果
url_part_1 = 'http://s.weibo.com/weibo/%25E6%2588%2591%25E5%2585%258D%25E8%25B4%25B9%25E5%259B%25B4%25E8%25A7%2582%25E4%25BA%2586&b=1&nodup=1'
# 搜索‘我免费围观了’的微博结果
wd.get(url_part_1)
set_2 = set()
n = 1
try:
    for element in wd.find_elements_by_class_name('W_btn_c6'):
        set_2.add(element.get_attribute('href'))
        print(str(n)+': '+element.get_attribute('href'))
        n = n+1
except:
    pass

t = 1
while t <= 48:
    t = t+1
    url_part_2 = '&page=%d'%t
    try:
        wd.get(url_part_1+url_part_2)
        time.sleep(random.randint(3,8))
        for element in wd.find_elements_by_class_name('W_btn_c6'):
            url = element.get_attribute('href')
            set_2.add(url)
            print(str(n)+': '+url)
            n = n+1
    except:
        pass

# 清除重复问题的url链接
s1 = set()
with open('weibo_1_utf-8.csv', 'r+', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        s1.add(row['page_url'])

s2 = set()
with open('weibo_new_page_url.csv', 'r', encoding='utf-8') as f1:
    reader = csv.DictReader(f1)
    for row in reader:
        s2.add(row['page_url'])


s3 = set_2 - s1 - s2
group = []
for part in s3:
    group.append([part])
with open('weibo_new_page_url.csv', 'a+', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in group:
        writer.writerow(row)
wd.close()
