import calendar

import pandas as pd
import gensim

from pymongo import MongoClient

client = MongoClient('localhost', 40001)
db = client['newsdb']
articles = db['articles']
i = 0
art = articles.find({}, {"_id": 1, "description": 1})
description_list = [doc['description'] for doc in art if doc['description'] is not None]
big_desc_str = ' '.join(description_list)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words as words_en
st_wrd = set(stopwords.words('english'))

tokens = word_tokenize(big_desc_str)

calldwr = [wd.lower() for wd in list(calendar.day_name)]

words = [word.lower() for word in tokens
         if word.isalpha()
         and word.lower() not in st_wrd
         and len(word) >= 3
         and word.lower() not in calldwr]

wordfreq = {}
for w in words:
    if w not in wordfreq:
        wordfreq.update({w: words.count(w)})

wordfreq_sorted = sorted(wordfreq.items(), key=lambda item: item[1], reverse=True)

sorted_dict = {w[0]: w[1] for w in wordfreq_sorted}
sorted_df = pd.DataFrame.from_dict(sorted_dict, orient='index')
sorted_df.to_pickle('data/wordcount_data')

model = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)

vector_list = [model[word] for word in words if word in model.vocab]

# Create a list of the words corresponding to these vectors
words_filtered = [word for word in words if word in model.vocab]

# Zip the words together with their vector representations
word_vec_zip = zip(words_filtered, vector_list)

# Cast to a dict so we can turn it into a DataFrame
word_vec_dict = dict(word_vec_zip)
df = pd.DataFrame.from_dict(word_vec_dict, orient='index')
df.to_pickle('data/dataframe');
