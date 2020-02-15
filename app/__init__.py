from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)
users = dict()
rooms = dict()
messages = dict()

from app import routes, sockets
