import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.manifold import TSNE

wordcount_df = pd.read_pickle('data/wordcount_data')
vector_df = pd.read_pickle('data/dataframe')

client = MongoClient('localhost', 40001, retryWrites=False)
newsdb = client['newsdb']
articles_coll = newsdb['articles']

start_date = 22
articles_curs = articles_coll.find(
    {"publishedAt": {"$gt": '2020-05-{:02d}T00:00:00'.format(start_date)}}, {'description': 1})
articles = list(articles_curs)

from nltk.tokenize import word_tokenize

dictionary = {}


def vec_repr_of_sentence(sentence):
    sentence_vec = np.zeros(300)
    wordlist = word_tokenize(sentence)
    list_of_vectors = [vector_df.loc[word, :].values for word in wordlist if word in vector_df.index.values]
    if len(list_of_vectors) == 0:
        return None
    sentence_vec = np.mean(list_of_vectors, axis=0)
    return sentence_vec


for art in articles[:500]:
    if art['description'] is not None:
        sentence = art['description']
        vec = vec_repr_of_sentence(sentence)
        if vec is not None:
            dictionary[sentence] = []
            dictionary[sentence].extend(list(vec))

sentence_df = pd.DataFrame.from_dict(dictionary, orient='index')

tsne = TSNE(n_components=2, init='random',learning_rate=500, random_state=10, perplexity=50)
tsne_df = tsne.fit_transform(sentence_df)

sns.set()
# Initialize figure
fig, ax = plt.subplots(figsize=(12, 9))
sns.scatterplot(tsne_df[:, 0], tsne_df[:, 1], alpha=0.5)

named_plot_data = {sentence_df.index.values[i]: [tsne_df[i, 0], tsne_df[i, 1]]
                   for i in range(len(sentence_df.index.values))}
from adjustText import adjust_text

texts = []
words_to_plot = wordcount_df[:20]
print(words_to_plot.index.values)
for sentence in sentence_df.index.values:
    print(sentence)
    sentence_words = word_tokenize(sentence)
    pop_words_count = 0
    for word in words_to_plot.index.values:
        if word in sentence_words:
            pop_words_count += sentence_words.count(word)
    if pop_words_count >= 4:
        article_title = articles_coll.find({'description': sentence}, {'title': 1})[0]['title']
        print(article_title)
        texts.append(plt.text(named_plot_data[sentence][0], named_plot_data[sentence][1], article_title[:20] + "...", fontsize=8))

print('ended sentence analysis')
adjust_text(texts, expand_points=(1, 1), expand_text=(1, 2),
            arrowprops=dict(arrowstyle="-", color='black', lw=1))
print('ended adj text')
plt.show()
