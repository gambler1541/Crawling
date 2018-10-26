import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


file_path = 'episode_list.html'
url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
params = {
    'titleId': 703845,
}

if not os.path.exists(file_path):
    response = requests.get(url_episode_list, params)
    html = response.text
    open(file_path, 'wt').write(html)
else:
    html = open('episode_list.html', 'rt').read()

soup = BeautifulSoup(html, 'lxml')

h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
desc = soup.select_one('div.detail > p').get_text()

table = soup.select_one('table.viewList')
tr_list = table.select('tr')
for index, tr in enumerate(tr_list[1:]):
    if tr.get('class'):
        continue

    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    # no를 가져오기 위해 url.parse를 사용
    url_dict_query = dict(parse.parse_qsl(parse.urlsplit(url_detail).query))
    no = url_dict_query.get('no')
    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    created_data = tr.select_one('td:nth-of-type(4)').get_text(strip=True)


