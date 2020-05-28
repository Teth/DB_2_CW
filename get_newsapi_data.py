import requests
from pymongo import MongoClient

client = MongoClient('localhost', 40001, retryWrites=False)

sources_arr = ['cnn',
               'fox-news',
               'reuters', ]
sources_arr2 = ['bbc-news',
                'bloomberg',
                'msnbc', ]
sources_arr3 = ['the-hill',
                'the-wall-street-journal',
                'vice-news', ]
sources_arr4 = ['the-washington-times',
                'the-huffington-post',
                'business-insider']

db = client["newsdb"]
articles_coll = db["articles"]
sources = ','.join(sources_arr4)
date = 1;

days = 25;
for i in range(days):
    new_date = date + i;
    for hrs in [0, 6, 12, 18]:
        hour = hrs
        new_min = 00
        new_hour = hrs + 6
        if new_hour == 24:
            new_hour = 23
            new_min = 59
        url = 'https://newsapi.org/v2/everything?sources={}&from=2020-05-{}T{}:00:00&to=2020-05-{}T{}:{}:00' \
              '&sortBy=popularity&pageSize=100&apiKey=a8d4dac8c59349c79fbaeb9989f1e60d' \
            .format(sources, new_date, hour, new_date, new_hour, new_min)
        print(url)
        resp_articles = requests.get(url)
        articles = resp_articles.json()['articles']
        # print(articles)
        for article in articles:
            articles_coll.insert_one(article)
