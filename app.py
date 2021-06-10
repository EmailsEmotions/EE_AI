import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return "Emails without emotions"


@app.route('/countFormal', methods=['POST'])
def formal_count():
    bekonez = {'formal': 0, 'informal': 0}
    data = request.get_data(as_text=True)
    for word in data.split():
        for key in bekonez:
            if word == key:
                bekonez[key] += 1

    return jsonify(bekonez)


@app.route('/countEmotions', methods=['POST'])
def emotions_count():
    emotions = {'happy': 0, 'sad': 0, 'fear': 0, 'angry': 0, 'surprise': 0, }
    data = request.get_data(as_text=True)
    for word in data.split():
        for key in emotions:
            if word == key:
                emotions[key] += 1

    return jsonify(emotions)
