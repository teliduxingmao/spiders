import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
import pymongo
from config import *

proxy = None
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_proxy():
    try:
        response = requests.get('http://127.0.0.1:5000/get')
        if response.status_code == 200:
            response = response.text
            print('Using Proxy:'+ response)
            return response
        else:
            print('there is no proxy to be used')
            return  None
    except ConnectionError:
        return None

def get_html(page,keyword):
    global proxy
    url = 'http://weixin.sogou.com/weixin?'
    params = {
        'query':keyword,
        'type':2,
        'page':page
    }
    headers = {
        'Cookie':'IPLOC=CN3100; SUID=57135E725018910A0000000059D34A96; SUV=1507019415055086; SNUID=CA8EC3EF9D9BC43ED3E372559EFA0750; ABTEST=5|1507019455|v1; JSESSIONID=aaaQbz4tq-V84_nyshz6v; wapsogou_qq_nickname=; ld=iZllllllll2B11$klllllVXFvs7llllltOcFqZllllyllllllZlll5@@@@@@@@@@; LSTMV=348%2C152; LCLKINT=2503; weixinIndexVisited=1; sct=6; ppinf=5|1507020627|1508230227|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0NTolRTclODklQjklRTclQUIlOEIlRTclOEIlQUMlRTglQTElOEMlRTclOEMlQUF8Y3J0OjEwOjE1MDcwMjA2Mjd8cmVmbmljazo0NTolRTclODklQjklRTclQUIlOEIlRTclOEIlQUMlRTglQTElOEMlRTclOEMlQUF8dXNlcmlkOjQ0Om85dDJsdUUzT1QwTmJJRFRRa0lPdDZDSzhVQjBAd2VpeGluLnNvaHUuY29tfA; pprdig=exDnoTQJ3Q8BWeSop3f7E1dKReiyUnFr5PJ3Fy_fhQn8nQ_MgkLhRnigi2MFG2Yl6GaSKYve03_ZzoLeiGPqiFc1JNLPUEyRCzhCiJKU2-Pubg_IPw_Yci3pMSF3JcExQHJyuckpIC3u3qMbW1M4fBXZRA1RilNJJ822iwVlZW4; sgid=00-36226635-AVnTT1PribyiaDN0JX5CDhIEI; ppmdig=1507020628000000d8b164b69ea6af36d863c7cc77ce7ccb',
        'Host':'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    try:
        if not proxy:
            response = requests.get(url,allow_redirects = False,params = params,headers = headers)
        else:
            proxies = {'http':'http://'+ proxy}
            response = requests.get(url, allow_redirects=False, params=params, headers=headers,proxies = proxies)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        if response.status_code == 302:
            print(302)
            #need proxy
            proxy = get_proxy()
            if proxy:
                return get_html(page,keyword)
            else:
                print('get proxy failed')
    except ConnectionError as e:
        print('访问失败',e.args)
        proxy = get_proxy()
        return get_html(page,keyword)

def parse_html(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_article_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('访问以下链接错误' + url)

def parse_article_detail(html):
    doc = pq(html)
    title = doc('#activity-name').text()
    content =doc('.rich_media').text()
    date =doc('#post-date').text()
    wechat =doc('#post-user').text()
    data = {
        'title':title,
        'content':content,
        'date':date,
        'wechat':wechat
    }
    return data

def save_to_mongo(data):
    if db[MONGO_TABLE].update({'title':data['title']},{'$set':data},True):
        print("Saved to Mongo",data['title'])
    else:
        print("Saved to Mongo Failed",data['title'])


def main():
    for i in range(1,PAGE_COUNT+1):
        html = get_html(i,KEY_WORD)
        article_urls = parse_html(html)
        for url in article_urls:
            html = get_article_html(url)
            data = parse_article_detail(url)
            save_to_mongo(data)


if __name__ == '__main__':
    main()