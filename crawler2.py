import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, no, title, rating, created_data):
        self.no = no
        self.title = title
        self.rating = rating
        self.created_data = created_data


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._html = None
        self._episode_list = list()

    def _get_info(self, attr_name):
        """
        해당 인스턴스에 인자로오는 속성이 있는지를 검사
        없으면 set_info()실행
        :return:
        """
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def html(self):
        # self._html이 Flase일 경우
        if not self._html:
            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
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
            # sefl._html을 채움
            self._html = html
        return self._html


    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    def set_info(self):
        """
        실제로 웹툰정보를 크롤링하는 함수
        인스턴스의 title, author, description을 채움
        :return:
        """
        soup = BeautifulSoup(self.html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')

        self._title = h2_title.contents[0].strip()
        self._author = h2_title.contents[1].get_text(strip=True)
        self._description = soup.select_one('div.detail > p').get_text()


    def get_episode_list(self):
        soup = BeautifulSoup(self.html, 'lxml')

        table = soup.select_one('table.viewList')

        tr_list = table.select('tr')
        epi_list = list()
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
            episode = Episode(
                no = no,
                title = title,
                rating = rating,
                created_data = created_data
            )
            epi_list.append(episode)
        self._episode_list = epi_list


    @property
    def episode_list(self):
        if not self._episode_list:
            self.get_episode_list()
        return self._episode_list



if __name__ == '__main__':
    a = Webtoon(703846)
    for epi in a.episode_list:
        print(epi.title)