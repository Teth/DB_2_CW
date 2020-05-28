import pandas as pd
import matplotlib.pyplot as plt

wordcount_df = pd.read_pickle('data/wordcount_data')

words_to_display = list(wordcount_df.index.values)[:40]
data_of_words_to_display = [wordcount_df.loc[w, 0] for w in words_to_display]

plt.figure(figsize=(8,9))
plt.xticks(range(len(words_to_display)), words_to_display, rotation='vertical')
plt.bar(range(len(data_of_words_to_display)), data_of_words_to_display, align='center')
plt.show()
quit()


