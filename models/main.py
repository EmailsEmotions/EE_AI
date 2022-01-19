import string

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gensim.models import KeyedVectors
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from stempel import StempelStemmer
from stop_words import get_stop_words

PREDICTED_EMOTION = 'formal'

print("Started loading word2vec...")
word2vec = KeyedVectors.load_word2vec_format("cc.pl.300.vec", binary=False)
print(word2vec)

stemmer = StempelStemmer.polimorf()
stop_words = get_stop_words('polish')

texts = pd.read_csv("texts.csv", sep=';', usecols=['text', PREDICTED_EMOTION])
texts[PREDICTED_EMOTION] = texts[PREDICTED_EMOTION].div(2.0)
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


texts_vectors[PREDICTED_EMOTION + '_class'] = texts[PREDICTED_EMOTION].multiply(2.0).round()
print(texts_vectors)

train_x, test_x, train_y, test_y = train_test_split(texts_vectors.drop(PREDICTED_EMOTION + "_class", axis=1),
                                                    texts_vectors[PREDICTED_EMOTION + "_class"],
                                                    test_size=0.1)
print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)

ada = AdaBoostClassifier(n_estimators=100)
decision_tree = DecisionTreeClassifier(min_samples_split=5, min_samples_leaf=2)
random_forest = RandomForestClassifier(min_samples_split=5, min_samples_leaf=2)

for model, name in zip([ada, random_forest, decision_tree],
                       ['Ada Boost Classifier', 'Decision Tree Classifier', 'Random Forest Classifier']):
    model.fit(train_x, train_y)
    test_pred = model.predict(test_x)
    train_pred = model.predict(train_x)

    print("=============================")
    print(name)

    print("Train ACC: " + str(accuracy_score(train_y, train_pred)))
    print(confusion_matrix(train_y, train_pred))

    print("Test ACC: " + str(accuracy_score(test_y, test_pred)))
    print(confusion_matrix(test_y, test_pred))

    cmt = confusion_matrix(test_y, test_pred)
    print(cmt)

    plt.subplots(figsize=(8, 6))
    plot = sns.heatmap(cmt, annot=True, cmap='Blues', fmt='g')
    plot.set_title('Macierz pomyłek - szczęśie')
    plot.set_xlabel('Przewidziany poziom szczęśia')
    plot.set_ylabel('Prawdziwy poziom szczęścia')
    plot.xaxis.set_ticklabels(['brak szczęścia', 'niewiele szczęścia', 'dużo szczęścia'])
    plot.yaxis.set_ticklabels(['brak szczęścia', 'niewiele szczęścia', 'dużo szczęścia'])
    plt.show()
