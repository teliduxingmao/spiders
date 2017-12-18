import requests,re
from pyquery import PyQuery as pq
from settings import  *
import urllib.parse
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

# res = requests.get(url = 'http://www.huangye88.com/search.html?kw=%E7%BD%91%E7%AB%99%E5%BB%BA%E8%AE%BE&type=company&page=1',headers = headers).text
#
# # print(res)
# pages = re.findall('<span class="text">共(.*?)页',res)[0]
# print(pages)
# keyword = urllib.parse.quote(KEYWORD)
# type = TYPE
# url = 'http://www.huangye88.com/search.html?kw={keyword}&type={type}&page={page}/'
# url = url.format(keyword = keyword,type = type,page = 1)
# print(url)

def add(a,b):
    a=1
    b=2
c = add(1,2)
print(c)
