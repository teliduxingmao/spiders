import json
import re,os,pymongo
from multiprocessing import Pool

from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from hashlib import md5
from requests import RequestException
from config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
def sava_to_mongodb(result):
    if db[MONGO_TABLE].insert(result):
        # print('Successfully Saved to Mongo'+ str(result))
        return True
    else:
        return False
def down_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None

def save_image(content):
    file_path ='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    print(file_path)
    with open(file_path,"wb") as f:
        f.write(content)
        f.close()
#根据初始链接，以text返回得到的网页内容
def get_page_source(offset,keyword):
    program = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(program)
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
        return None
    except RequestException:
        print("访问出错")
    return None
#返回详情网页的text
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
        return None
    except RequestException:
        print("访问详情页出错"+url)
#返回由title,url,image_url_list构成的字典
def parse_page_detail(html,url):
    soup = BeautifulSoup(html)
    title = soup.title.get_text()
    print(title)
    image_pattern = re.compile('gallery:\s(.*?)siblingList',re.S)
    result = re.search(image_pattern,html)
    if result:
        result = result.group(1).strip()[:-1]
        data = json.loads(result)
        if data and 'sub_images' in data:
            image_url_list = data.get('sub_images')
            image_url_list = [item['url'] for item in image_url_list]
            print(image_url_list)
            for url in image_url_list:
                down_image(url)
            return {
                'title':title,
                'url':url,
                'image_url_list':image_url_list
            }


#以可迭代对象返回每个组图的总链接
def parse_page_source(html):
    result = json.loads(html)
    if result and 'data' in result.keys():
        for item in result.get("data"):
            yield item.get("article_url")

def main(offset):
    html = get_page_source(offset,KEYWORD)
    urls = parse_page_source(html)
    for url in urls:
        html = get_page_detail(url)
        result = parse_page_detail(html,url)
        if result:sava_to_mongodb(result)

if __name__ == "__main__":
    pool = Pool()
    pool.map(main,[i*10 for i in range(GROUP_START,GROUP_END+1)])
    pool.close()
    pool.join()


