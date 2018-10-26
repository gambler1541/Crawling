import os

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        info = self.webtoon_crawler()
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']

    def webtoon_crawler(self):
        '''
        webtoon_id 매개변수를 이용하여
        웹툰 title, authorm description를 딕셔너리를 형태로 return
        :return:
        '''
        file_path= 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
        params = {
            'titleId': self.webtoon_id,
        }
        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            response = requests.get(url_episode_list, params)
            html = response.text
            open(file_path, 'wt').write(html)

        soup = BeautifulSoup(html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')

        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text()

        return {
            'title': title,
            'author': author,
            'description': description
        }


if __name__ == '__main__':
    a= Webtoon(25455)
    print(a.title)
    print(a.author)
    print(a.description)
