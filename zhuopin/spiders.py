import requests,time
from pyquery import PyQuery as pq
import pymongo
import urllib.parse
from multiprocessing import Pool
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

start_url = 'http://www.highpin.cn/zhiwei/rt_2_p_{page}_zw_{keyword}.html'
string = 'route=8aef807f4c105cb112ad9767652f581b; tencentSig=8770857984; Guid_Cookie_Identity=HighEnd_Identity=92cafff3-5d82-4915-8614-e5e0a5f49ada; dywez=162498211.1509364189.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; gr_user_id=6054de7c-2ab4-4d6a-bcb7-5585c4c52306; pgv_pvi=806715392; pgv_si=s5562536960; IESESSION=alive; jobsInfoShowLogin=hide; route=3c43908337e0716685321d8c47c83c79; _qddamta_800006744=3-0; __utmt=1; SearchCoditions=Title=%e6%80%bb%e7%bb%8f%e7%90%86%2b%e4%bc%81%e4%b8%9a%e8%81%8c%e4%bd%8d&Url=http%3a%2f%2fwww.highpin.cn%2fzhiwei%2frt_2_p_1_zw_%25E6%2580%25BB%25E7%25BB%258F%25E7%2590%2586.html; __xsptplusUT_158=1; __xsptplus158=158.4.1509448615.1509449525.12%234%7C%7C%7C%7C%7C%23%23hLpnXyjJxvXIxbBcVjGPOIh9klqu909f%23; dywea=162498211.3286544520665608700.1509364189.1509374391.1509448616.4; dywec=162498211; dyweb=162498211.6.10.1509448616; _uniut_id.1002=955d20b973982110%7C1509364189%7C1%7C1509449525%7C1509378920%7C49115E72044DC759F711DA; _uni_id=49115E72044DC759F711DA; Hm_lvt_6d73053c6b28df9b631301488842df9a=1509364208; Hm_lpvt_6d73053c6b28df9b631301488842df9a=1509449525; __utma=107384859.941700006.1509364208.1509374391.1509448616.4; __utmb=107384859.6.10.1509448616; __utmc=107384859; __utmz=107384859.1509364208.1.1.utmcsr=c.highpin.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; gr_session_id_48b131d0b0794621aaf54d7bfb8991bb=e9f08886-c334-4d48-814c-9bd7f340ce21; gr_cs1_e9f08886-c334-4d48-814c-9bd7f340ce21=user_id%3A; NSC_ijhiqjo-172.19.0.190=ffffffffaf1b1c4d45525d5f4f58455e445a4a423660; _qddaz=QD.ftoe9w.umqnk1.j9e4gtze; _qdda=3-1.3msy0w; _qddab=3-zfnbr.j9fiqdoo'
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'www.highpin.cn',
        'Referer': 'http://www.highpin.cn/zhiwei/rt_2_p_116_zw_%E6%80%BB%E7%BB%8F%E7%90%86.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Connection': 'keep-alive'
    }
def turn_to_cookies(string):
    cookies = {}
    for item in string.split(';'):
        name,value = item.strip().split('=',1)
        cookies[name] = value
    return cookies
cookies = turn_to_cookies(string)

def get_index(start_url,count):
    if count<10:
        # proxy = get_proxy()
        html = requests.get(url = start_url, headers = headers,cookies = cookies)
        if html.status_code !=200:
            count += 1
            return get_index(start_url,count)
        doc = pq(html.text)
        zhiwei_list = doc('.c-job-box .c-list-box .jobInfoItem .jobname a')
        for item in zhiwei_list.items():
            href = item.attr.href
            print(href)
            yield href
    return None


def parse_details(url):
    time.sleep(2)
    url = 'http://www.highpin.cn/'+ url
    try:
        html = requests.get(url = url,headers = headers,cookies = cookies,timeout = 10).text
    except ConnectionError:
        return
    doc = pq(html)
    item = {}
    item['job'] = doc('h1 .cursor-d ').text()
    item['company'] = doc('.mainContent').children('.c-view-module')('.innerSite_link').text()
    item['basic_information'] = doc('.mainContent .mb_15 div:nth-child(1)').text()
    item['payment'] = doc('.mainContent .mb_15 .c-view-module:nth-child(2)').text()
    item['job_description'] = doc('.mainContent .mb_15 .c-view-module:nth-child(3)').text()
    item['other_information'] = doc('.mainContent .mb_15 .c-view-module:nth-child(4)').text()
    item['company_introduction'] = doc('.mainContent .mb_15 .c-view-module:nth-child(5)').text()
    print(item['job'])
    save_to_mongo(item)

def save_to_mongo(data):
    client = pymongo.MongoClient('localhost:27017')
    db = client['zhilianzhuopin']
    if data:
        if (not '助理' in data['job'] ) and (not '秘书' in data['job']) and ('总经理' in data['job'] or '总裁' in data['job'] or '副总经理' in data['job'] or '副总裁' in data['job']):
            if db['job'].insert(data):
                print('saved to mongo:'+ data['job'])

def get_total(keyword):
    url = start_url.format(page=1, keyword=keyword)
    print(url)
    response = requests.get(url=url, headers=headers,cookies = cookies).text
    print(response)
    doc = pq(response)
    return int(doc('.c-pagebox .c-pagebtn ul li:nth-child(6)').text())

def main(keyword):

    n = get_total(keyword)
    print(n)
    for i in range(1,n+1) :
        url = start_url.format(page = i,keyword = keyword)
        print(url)
        for url in get_index(url,0):
            parse_details(url)

if __name__ == '__main__':
    # pool = Pool()
    list = ['总经理','总裁','副总经理','副总裁']
    list = [urllib.parse.quote(string) for string in list]
    # pool.map(main,list)
    # pool.close()
    # pool.join()
    for keyword in list:
        main(keyword)
