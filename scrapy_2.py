import time
from selenium import webdriver
import csv
import re
from selenium.common.exceptions import TimeoutException
import pymysql

csv_read_path = 'weibo_new_page_url.csv'
conn = pymysql.connect(host='localhost', user='root', password='herik', database='weibodata', charset='utf8mb4')
cur = conn.cursor()
cur.execute('use weibodata')

# 获取问题的围观数量和打赏数量
chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
wd = webdriver.Chrome(executable_path=chromePath)  # 构建浏览器
wd.set_page_load_timeout(30)
loginUrl = 'http://www.weibo.com/login.php'

wd.get(loginUrl) # 进入登陆界面
time.sleep(5)
wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('13777015316')  # 输入用户名
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('595432157')  # 输入密码
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()  # 点击登陆
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(input("输入验证码： "))
# wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()#再次点击登陆

time.sleep(20)  # 等待20秒用于输入验证码

n = 0  # 计数器
with open(csv_read_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        page_url = row['page_url']
        onlooker_num = '0'
        reward_num = '0'
        n = n+1
        try:
            wd.get(page_url)
            try:
                onlooker_description = wd.find_element_by_xpath(
                    '//*[@id="plc_main"]/div/div/div/div/div[3]/div[3]/div/div/p').text
                onlooker_num = re.findall(".*...等(.*)人.*", onlooker_description.split('，')[0])[0]
                if '，' in onlooker_description:
                    reward_num = onlooker_description.split('，')[1][4:-1]
                else:
                    reward_num = '0'
            except Exception:
                pass
            try:
                onlooker_description = wd.find_element_by_xpath(
                    '//*[@id="plc_main"]/div/div/div/div/div[2]/div[3]/div/div/p').text
                onlooker_num = re.findall(".*...等(.*)人.*", onlooker_description.split('，')[0])[0]
                if '，' in onlooker_description:
                    reward_num = onlooker_description.split('，')[1][4:-1]
                else:
                    reward_num = '0'
            except:
                pass
        except TimeoutException:
            wd.execute_script('window.stop()')  # 页面加载超时后停止加载

        print(str(n) + ': ' + str([reward_num, onlooker_num]))
        cur.execute("insert into weibo_scrapy_2(page_url, reward_num, onlooker_num) values(\"%s\", %s, %s)", (page_url, reward_num, onlooker_num))
        # 将数字类型数据传入sql语句时，去掉引号，同时使用字符串传入数字数据
        cur.connection.commit()

cur.close()
conn.close()
wd.close()
