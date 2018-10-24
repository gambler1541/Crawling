import requests

response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)
print(response.text)

with open('weekday.html', 'wt') as f:
    f.write(response.text)