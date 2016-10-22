import json

from flask import Flask, session
from flask_socketio import SocketIO, emit

from config import Config
from data import clients
from packet import Packet

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object(Config())
socketio = SocketIO(app)


@socketio.on("data")
def process(data):
    packet = Packet.parse(data)
    header, object = packet.handle()
    emit("data", "{:0>3}{}".format(header, json.dumps(object)))


@socketio.on("disconnect")
def disconnect():
    uid = session["uid"]
    if uid in clients:
        del clients[uid]
