import flask
from flask import request, jsonify
import py_eureka_client.eureka_client as eureka_client
import string
import random
from gensim.models import KeyedVectors
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import pickle
import os
from stop_words import get_stop_words

app = flask.Flask(__name__)
app.config["DEBUG"] = True
if os.environ.get('ENV', 0) == 'prod':
    eureka_server = "http://discovery-server:8761/eureka/,http://0.0.0.0:8761/eureka,http://host.docker.internal:8761/eureka,http://localhost:8761/eureka,http://127.0.0.1:8761/eureka,http://172.17.0.2:8761/eureka"
    instance_host="ai-service"
    print('PRODUCTION MODE')
else:
    eureka_server = "http://localhost:8761/eureka/"
    instance_host="127.0.0.1"
    print('TEST MODE')

# The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
eureka_client.init(eureka_server=eureka_server,
                   app_name="ai-service",
                   instance_host=instance_host,
                   instance_port=5600)

def prepare_text_for_learning(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', '1234567890'))
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split(' ')
    prepared_words = []

    for word in words:
        if len(word) > 1 and word and word not in stop_words:
            prepared_words.append(word)

    word_vectors = pd.DataFrame()
    for word in prepared_words:
        try:
            word_vec = word2vec[word]
            word_vectors = word_vectors.append(pd.Series(word_vec), ignore_index=True)
        except KeyError:
            pass

    return word_vectors.mean()


print("Welcome to Emails Emotions AI module!")

print("Loading and creating AI models from files.")
formality_model = pickle.load(open("models/exported/formal_Ada Boost Classifier_model.sav", 'rb'))
happy_model = pickle.load(open("models/exported/happy_Random Forest Classifier_model.sav", 'rb'))
angry_model = pickle.load(open("models/exported/angry_Ada Boost Classifier_model.sav", 'rb'))
fear_model = pickle.load(open("models/exported/fear_Random Forest Classifier_model.sav", 'rb'))
surprise_model = pickle.load(open("models/exported/surprise_Ada Boost Classifier_model.sav", 'rb'))
sad_model = pickle.load(open("models/exported/sad_Decision Tree Classifier_model.sav", 'rb'))
stop_words = get_stop_words('polish')
print("All AI models loaded successfully!")

print("Started loading Word2vec. This could take a while... (around 10 minutes)")
word2vec = KeyedVectors.load_word2vec_format("cc.pl.300.vec", binary=False)
print("Word2vec has been loaded successfully!")


@app.route('/')
def home():
    return "Emails emotions AI module"


@app.route('/countFormal', methods=['POST'])
def formal_count():
    text = request.get_data(as_text=True)
    text_features = prepare_text_for_learning(text)
    prediction = formality_model.predict([text_features])

    response = {
        'formal': prediction[0],
        'informal': 2 - prediction[0]
    }
    # response = {
    #     'formal': 1,
    #     'informal': 2 - 1
    # }
    return jsonify(response)


@app.route('/countEmotions', methods=['POST'])
def emotions_count():
    text = request.get_data(as_text=True)
    text_features = prepare_text_for_learning(text)

    response = {
        'happy': happy_model.predict([text_features])[0],
        'sad': sad_model.predict([text_features])[0],
        'fear': fear_model.predict([text_features])[0],
        'angry': angry_model.predict([text_features])[0],
        'surprise': surprise_model.predict([text_features])[0]
    }
    return jsonify(response)
