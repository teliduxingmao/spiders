import requests,re,pymongo
from pyquery import PyQuery as pq
from multiprocessing import Pool
import urllib.parse
from settings import *
from requests.exceptions import ConnectionError

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Referer':'http://www.huangye88.com/search.html?kw=%E7%BD%91%E7%AB%99%E5%BB%BA%E8%AE%BE&type=sale',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

def get_index(url):
    try:
        res = requests.get(url,headers = headers).text
    except ConnectionError:
        return None
    doc = pq(res)
    com = doc('.content .big-pro li .p-title a').items()
    for i in com:
        yield i.attr('href')

def parse_details(url):
    item = {}
    try:
        res = requests.get(url, headers=headers).text
    except ConnectionError:
        return item
    doc = pq(res)
    item['company'] = doc('body > div.cont > div.c-right > div:nth-child(1) > div.r-content > div > p ').text()
    try:
        product = re.findall('主营产品：</label>(.*?)</li>',res,re.S)[0]
        item['product'] = product
    except IndexError:
        print('这个公司找不到主营产品：'+item['company'])
    item['phone_number'] = doc('body > div.cont > div.c-left > div:nth-child(3) > div.l-content > ul > li:nth-child(4)').text()[
                   4:]
    item['qq_url'] = doc('body > div.cont > div.c-left > div:nth-child(3) > div.l-content > ul > li:nth-child(5) > a').attr('href')
    return item

def get_person(url):
    try:
        res = requests.get(url,headers = headers).text
    except ConnectionError:
        return None
    doc = pq(res)
    person = doc('body > div.cont > div.c-right > div:nth-child(1) > div.r-content > div > ul > li:nth-child(1) > a').text()
    return person

def get_qq(url):
    qq = re.findall('uin=(.*?)&site',url)[0]
    return qq

def save_to_mongo(item):
    client = pymongo.MongoClient('localhost')
    db = client['huangye88']
    if db['wangzhanjiashe'].update({'company':item['company']},item,True):
        print('save to mmongo:',item)

def main(url):
    for url in get_index(url):
        print(url)
        detail_url = url+'company_detail.html'
        contact_url = url+'company_contact.html'
        item = parse_details(detail_url)
        person = get_person(contact_url)
        item['person'] = person
        try:
            qq_url = item['qq_url']
            if qq_url:
                qq = get_qq(qq_url)
                item['qq'] = qq
                item.pop('qq_url')
                save_to_mongo(item)
        except KeyError:
            continue
def get_total(url):
    res = requests.get(url,headers = headers).text
    pages = re.findall('<span class="text">共(.*?)页', res)[0]
    return int(pages)

if __name__ == '__main__':
    pool = Pool()
    keyword = urllib.parse.quote(KEYWORD)
    type = TYPE
    url = 'http://www.huangye88.com/search.html?kw={keyword}&type={type}&page={page}/'
    total = get_total(url.format(keyword = keyword,type = type,page = 2))
    groups = ([url.format(keyword = keyword,type = type,page = i) for i in range(1,total+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()

