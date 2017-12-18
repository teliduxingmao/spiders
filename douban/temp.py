import requests,re
from pyquery import PyQuery as pq

url = 'https://movie.douban.com/subject/26580232/'
res = requests.get(url).text
doc = pq(res)
movie = doc('h1 span:first-child').text()
year = doc('h1 span:nth-child(2)').text()[1:-1]
director = doc('#info > span:nth-child(1) > span.attrs > a').text()
writers = doc('#info > span:nth-child(3) > span.attrs > a').text()
actors = doc('#info > span.actor').text()[4:]
type = doc('#info [property="v:genre"]').text()
country = re.findall('制片国家/地区:</span>(.*?)<br',res,re.S)[0]
language = re.findall('语言:</span>(.*?)<br',res,re.S)[0]
date = doc('#info [property="v:initialReleaseDate"]').text()
length = doc('#info [property="v:runtime"]').text()
grades = doc('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong').text()
five_stars = doc('#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per').text()
four_stars = doc('#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(2) > span.rating_per').text()
three_stars = doc('#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(3) > span.rating_per').text()
two_stars = doc('#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(4) > span.rating_per').text()
one_star = doc('#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(5) > span.rating_per').text()