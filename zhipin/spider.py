import requests,re,pymongo
from pyquery import PyQuery as pq
from settings import *

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

def get_start_url(city):
    city_dict = {
        '上海':'http://www.zhipin.com/c101020100/h_101020100/',
        '北京':'http://www.zhipin.com/c101010100/h_101010100/',
        '深圳':'http://www.zhipin.com/c101280600/h_101280600/',
        '广州':'http://www.zhipin.com/c101280100/h_101280100/',
        '杭州':'http://www.zhipin.com/c101210100/h_101210100/'
    }
    return city_dict[city]


def save_to_mongo(data):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    if db[MONGO_TB].insert(data):
        print('save to mongo:',data)

def parse_details(city,keyword,page = 1):
    url = get_start_url(city)
    params = {
        'query':keyword,
        'page':page
    }
    print(url)
    res = requests.get(url,headers = headers,params = params).text
    doc = pq(res)
    for item in doc('.job-list ul li').items():
        obj = {}
        result = item('.info-primary a').text().split(' ')
        obj['job'] = result[0]
        obj['payment'] = result[1]
        obj['company'] = item('.company-text a').text()
        result = item('.company-text p').text().split(' ')
        obj['industry'] = result[0]
        obj['financing_rounds'] = result[1]
        obj['number_of_people'] = result[-1]
        if obj['financing_rounds'] == obj['number_of_people']:
            obj['financing_rounds'] = None
        obj['reqirements'] = item('.info-primary p').text().split(' ')[1]
        print(obj)
        save_to_mongo(obj)
    nextpage = doc('#main > div.job-box > div.job-list > div.page > a.next').attr['href']
    if nextpage:
        page+=1
        return parse_details(city,keyword,page)
    else:
        return

def main(city,keyword):
    parse_details(city,keyword)

if __name__ == '__main__':
    city = CITY
    keyword = KEYWORD
    main(city,keyword)