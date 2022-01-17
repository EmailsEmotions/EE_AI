import string

import pandas as pd
from stempel import StempelStemmer
from stop_words import get_stop_words
from gensim.models import KeyedVectors

print("Started loading word2vec...")
word2vec = KeyedVectors.load_word2vec_format("cc.pl.300.vec", binary=False)
print(word2vec)

stemmer = StempelStemmer.polimorf()
stop_words = get_stop_words('polish')
texts = pd.read_csv("texts.csv", sep=';', usecols=['text', 'formal'])

texts['formal'] = texts['formal'].div(2.0)

texts_vectors = pd.DataFrame()
for index, text in texts.iterrows():
    print("Generating word vectors from texts:  " + str(index) + " / " + str(len(texts.index)))

    text['text'] = text['text'].lower()
    text['text'] = text['text'].translate(str.maketrans('', '', '1234567890'))
    text['text'] = text['text'].translate(str.maketrans('', '', string.punctuation))

    words = text['text'].split(' ')
    stemmed_words = []

    for word in words:
        if len(word) > 1 and word and word not in stop_words:
            stemmed_word = stemmer.stem(word)
            if stemmed_word is not None and stemmed_word not in stop_words:
                stemmed_words.append(stemmed_word)

    word_vectors = pd.DataFrame()
    for word in stemmed_words:
        try:
            word_vec = word2vec[word]
            word_vectors = word_vectors.append(pd.Series(word_vec), ignore_index=True)
        except KeyError:
            pass

    texts_vectors = texts_vectors.append(word_vectors.mean(), ignore_index=True)

    print(texts_vectors)

texts_vectors['formality'] = texts['formal']
print(texts_vectors)
