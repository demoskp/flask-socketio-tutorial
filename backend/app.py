from flask import Flask
from flask_socketio import emit, join_room, leave_room, rooms

from extensions import socketio

app = Flask(__name__)
app.config.from_object("config")
socketio.init_app(app, cors_allowed_origins="*")


@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})


@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    if room in rooms():
        emit('message', {'username': username, 'message': message}, to=room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('join', {'username': username}, to=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('leave', {'username': username}, to=room)


if __name__ == "__main__":
    socketio.run(app=app, debug=app.config.get("FLASK_DEBUG"))
