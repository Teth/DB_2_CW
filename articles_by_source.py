import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient('localhost', 40001, retryWrites=False)
newsdb = client['newsdb']
articles = newsdb['articles']

sources_arr = ['cnn',
               'fox-news',
               'reuters',
               'bbc-news',
               'bloomberg',
               'msnbc',
               'the-hill',
               'the-wall-street-journal',
               'vice-news',
               'business-insider']

result_dictionary = {
    'cnn': {'aggr': 0, 'arr': []},
    'fox-news': {'aggr': 0, 'arr': []},
    'reuters': {'aggr': 0, 'arr': []},
    'bbc-news': {'aggr': 0, 'arr': []},
    'bloomberg': {'aggr': 0, 'arr': []},
    'msnbc': {'aggr': 0, 'arr': []},
    'the-hill': {'aggr': 0, 'arr': []},
    'the-wall-street-journal': {'aggr': 0, 'arr': []},
    'vice-news': {'aggr': 0, 'arr': []},
    'business-insider': {'aggr': 0, 'arr': []}
}

date = 1
days = 25
for i in range(days):
    new_date = date + i;
    for hrs in [0, 6, 12, 18]:
        hour = hrs
        new_hour = hrs + 6
        if new_hour == 24:
            new_new_date = new_date + 1
            new_hour = 00
        else:
            new_new_date = new_date
        odate = '2020-05-{:02d}T{:02d}:00:00'.format(new_date, hour)
        ndate = '2020-05-{:02d}T{:02d}:00:00'.format(new_new_date, new_hour)
        print(odate)
        print(ndate)
        for source in sources_arr:
            print('...')
            cnt = articles.count_documents({"publishedAt": {"$gt": odate,
                                                            "$lt": ndate},
                                            "source.id": source})
            result_dictionary[source]['aggr'] += cnt
            if len(result_dictionary[source]['arr']) != 0:
                result_dictionary[source]['arr'].append(result_dictionary[source]['arr'][-1] + cnt)
            else:
                result_dictionary[source]['arr'].append(cnt)

aggr = 0
for key in result_dictionary.keys():
    aggr += result_dictionary[key]['aggr']

true_aggr = articles.count_documents({"publishedAt": {"$gt": "2020-05-01T00:00:00",
                                                      "$lt": "2020-05-26T00:00:00"}})

from scipy.ndimage.filters import gaussian_filter1d

plt.figure(figsize=(16, 9))
for key in result_dictionary.keys():
    ysmoothed = gaussian_filter1d(result_dictionary[key]['arr'], sigma=1.15)
    plt.plot(ysmoothed, label=key, linewidth=2.2)

plt.legend(result_dictionary.keys())
plt.show()