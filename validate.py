from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 40001)
db = client['newsdb']
articles = db['articles']

all = articles.find({}, {"_id": 1, "title": 1})

articles_titles = set()
for article in all:
    if article['title'] not in articles_titles:
        articles_titles.add(article['title'])
    else:
        articles.delete_one({'_id': ObjectId(article['_id'])})
