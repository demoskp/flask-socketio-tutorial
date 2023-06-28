from flask import Flask
from flask_socketio import rooms, emit, join_room, leave_room

from extensions import socketio

app = Flask(__name__)
app.config.from_object("config")
socketio.init_app(app)


@socketio.on("connect")
def on_connect(auth):
    if auth.get("token") != "123":
        raise ConnectionRefusedError("unauthorized!")


@socketio.on("message")
def handle_message(data):
    username = data.get("username")
    message = data.get("message")
    room = data.get("room")
    if room in rooms():
        emit("message", {"username": username, "message": message}, to=room)


@socketio.on("join")
def on_join(data):
    username = data.get("username")
    room = data.get("room")
    join_room(room)
    emit("join", {"username": username}, to=room)


@socketio.on("leave")
def on_leave(data):
    username = data.get("username")
    room = data.get("room")
    leave_room(room)
    emit("leave", {"username": username}, to=room)


if __name__ == "__main__":
    socketio.run(app=app, debug=app.config.get("FLASK_DEBUG"), host="0.0.0.0", port=5555)
