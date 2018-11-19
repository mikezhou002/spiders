# coding:utf-8

import requests
from pyquery import PyQuery as pq
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
headers = {'User-Agent':User_Agent}
url = 'https://www.91160.com/search/index/ulvl-0/ht-0/disease_id-0/utype-0/aid-7/isopen-1/ysort-1/cid-5.html'
session = requests.session()
r = session.get(url, headers=headers)
print r.status_code
print len(r.text)
doc = pq(r.text)
result = doc('h2 a').text()
print result


