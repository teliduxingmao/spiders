import  requests,re,json,time
from multiprocessing import  Pool
url0 = "http://maoyan.com/board/4?offset="

def get_movie(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
    html = requests.get(url = url, headers=headers).text
    pattern = re.compile('<dd.*?name.*?href="(.*?)".*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">.*?</dd>',re.S)
    lis = re.findall(pattern,html)
    print(lis)
    return lis
def write_in(content):
    for url,title,actor in content:
        url = 'http://maoyan.com'+url+' '
        title = title.strip()+' '
        actor = actor.strip()[3:]+' '
        with open("maoyan.txt",'a',encoding="utf-8") as  file:
            file.write(json.dumps(url+title+actor,ensure_ascii=False)+'\n')
            file.close()
def main(offset):
    url = url0 + str(offset)
    print(url)
    content = get_movie(url)
    write_in(content)
if __name__ == '__main__':
    for i in range(0,10):
        main(i*10)
    # pool = Pool()
    # pool.map(main,[i*10 for i in range(0,10)])
