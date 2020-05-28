import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

vector_df = pd.read_pickle('data/dataframe')
wordcount_df = pd.read_pickle('data/wordcount_data')
# Initialize t-SNE
tsne = TSNE(n_components=2, init='random', random_state=10, perplexity=300)

# Use only 400 rows to shorten processing time
analyzed_data = vector_df[:3000]
tsne_df = tsne.fit_transform(analyzed_data)
words = analyzed_data.index.values
named_plot_data = {words[i]: [tsne_df[i, 0], tsne_df[i, 1]] for i in range(len(words))}

sns.set()
# Initialize figure
fig, ax = plt.subplots(figsize=(12, 9))
sns.scatterplot(tsne_df[:, 0], tsne_df[:, 1], alpha=0.5)

# Import adjustText, initialize list of texts
from adjustText import adjust_text

texts = []
words_to_plot = wordcount_df[:150].index.values

for word in words_to_plot:
    if word in named_plot_data.keys():
        val = named_plot_data[word]
        texts.append(plt.text(named_plot_data[word][0], named_plot_data[word][1], word, fontsize=8))

# Plot text using adjust_text (because overlapping text is hard to read)
adjust_text(texts, expand_points=(1, 1), expand_text=(1, 2),
            arrowprops=dict(arrowstyle="-", color='black', lw=1))

plt.show()