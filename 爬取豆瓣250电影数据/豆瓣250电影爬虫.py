import requests
from bs4 import BeautifulSoup
import pandas as pd
def get_douban_top250(url):
    h={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=h)
    response.encoding = 'utf-8'
    tree = BeautifulSoup(response.text, 'html.parser')
    data=tree.select('div.info')
    movie_list = []
    for item in data:
        title = item.select('span.title')[0].get_text()
        rating = item.select('span.rating_num')[0].get_text()
        type = item.select('div.bd p')[0].get_text().split('/')[-1].strip()
        director1 = item.select('div.bd p')[0].get_text()
        director2 = director1.split(';')[0].replace('导演:','').strip()
        director = director2.split('\xa0')[0]
        actor1 = item.select('div.bd p')[0].get_text().split(':')[-1].strip()
        actor = actor1.split('/...')[0]
        release_date = item.select('div.bd p')[0].get_text().split('/')[-3].strip()[-4:]
        num =item.select('div.bd span')[3].get_text()
        movie_list.append({'title': title, 'rating': rating, 'type': type, 'director': director, 'actor': actor, 'release_date': release_date, 'num': num})
    return movie_list
all_movies = []
urls = [f'https://movie.douban.com/top250?start={i}' for i in range(0, 250, 25)]
for url in urls:
     all_movies.extend(get_douban_top250(url))
df = pd.DataFrame(all_movies)
df.to_excel('douban_top250.xlsx', index=False)
print("爬取完成！结果已保存到 douban_top250.xlsx")

    
