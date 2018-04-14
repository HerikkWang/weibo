from bs4 import BeautifulSoup
import lxml
import html5lib
import Login
from urllib.request import urlopen
import csv

'''scrape the data, whose attributes include question_content, question_value, questioner_name, 
questioner_id, replier_name, replier_id, question_time'''

csv_write_path = r"C:\Users\Administrator\PycharmProjects\weibo\weibo_data_2_1.csv"
csv_read_path = 'weibo_data_4_processed.csv'


def get_data_1(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html.read(),'lxml')
        question_content = bsObj.find('div',{'class':'ask_con'}).get_text().strip()
        question_value = bsObj.find('em',{'class':'S_spetxt'}).get_text().strip()[1:]
        questioner_name = bsObj.find_all('a',{'class':'S_txt1'})[1].get_text().strip()
        questioner_id = bsObj.find_all('a',{'class':'S_txt1'})[1].attrs['href'][3:]
        replier_name = bsObj.find_all('a',{'class':'S_txt1'})[3].get_text().strip()
        replier_id = bsObj.find_all('a',{'class':'S_txt1'})[3].attrs['href'][3:]
        question_time = bsObj.find('div',{'class':'S_txt2'}).get_text()[:-2]
    except:
        question_content = ''
        question_value = ''
        questioner_name = ''
        questioner_id = ''
        replier_id = ''
        replier_name = ''
        question_time = ''
    data = [question_content, question_value, questioner_name, questioner_id, replier_name, replier_id, question_time]
    return data
    # print(question_content+'\n'+question_value+'\n'+questioner_name+'\n'+questioner_id+'\n'
          # +replier_name+'\n'+replier_id+'\n'+question_time)

Login.login()
datas = [['question_content', 'question_value', 'questioner_name', 'questioner_id', 'replier_name', 'replier_id', 'question_time', 'page_url']]
with open(csv_read_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        page_url = row['page_url']
        data = get_data_1(page_url)
        data.append(page_url)
        datas.append(data)

with open(csv_write_path, 'w+', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in datas:
        writer.writerow(row)