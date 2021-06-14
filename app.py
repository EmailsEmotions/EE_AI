import flask
from flask import request, jsonify
import py_eureka_client.eureka_client as eureka_client


app = flask.Flask(__name__)
app.config["DEBUG"] = True

your_rest_server_port = 80
# The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
eureka_client.init(eureka_server="http://discovery-server:8761/eureka/,http://0.0.0.0:8761/eureka,http://host.docker.internal:8761/eureka",
                   app_name="ai-service",
                   instance_port=your_rest_server_port)

@app.route('/')
def home():
    return "Emails without emotions"


@app.route('/countFormal', methods=['POST'])
def formal_count():
    bekonez = {'formal': 0, 'informal': 0}
    data = request.get_data(as_text=True)
    max = 1
    for word in data.split():
        for key in bekonez:
            if word == key:
                bekonez[key] += 1
            if(bekonez[key] > max):
                max=bekonez[key]
    for key in bekonez:
        bekonez[key]/=max
    return jsonify(bekonez)


@app.route('/countEmotions', methods=['POST'])
def emotions_count():
    emotions = {'happy': 0, 'sad': 0, 'fear': 0, 'angry': 0, 'surprise': 0, }
    data = request.get_data(as_text=True)
    max = 1
    for word in data.split():
        for key in emotions:
            if word == key:
                emotions[key] += 1
            if(emotions[key] > max):
                max=emotions[key]
    for key in emotions:
        emotions[key]/=max
    return jsonify(emotions)
