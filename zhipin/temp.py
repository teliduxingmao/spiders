import requests,re,pymongo
from pyquery import PyQuery as pq


url = 'http://www.zhipin.com/c101020100/h_101020100/?query=python&page=3&ka=page-3'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
url = 'http://www.zhipin.com/c101210100/h_101210100/'
params = {
    'query':'python',
    'page':1
}
res = requests.get(url,params=params,headers = headers).text
print(res)