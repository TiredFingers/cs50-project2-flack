from app import socketio, users, rooms, messages
from flask_socketio import join_room, leave_room, send, emit
import time


@socketio.on("join")
def join_handler(data):

    join_room(data["room"])

    room_messages = messages[data["room"]] if data["room"] in messages else {}
    payload = {"messages": room_messages, "username": data["username"]}

    socketio.emit("all-room-msgs",
                  payload,
                  room=data["room"])


@socketio.on("leave")
def leave_handler(data):
    leave_room(data["room"])


@socketio.on("create-room")
def create_room_handler(data):

    if data["room"] in rooms:
        return {"error": "room exists"}
    else:
        rooms[data["room"]] = True
        return {"room": data["room"]}


@socketio.on("delete-room")
def delete_room_handler(data):
    rooms.pop(data["room"], None)


@socketio.on("message")
def message_handler(message):

    msg_list = [message["user"], message["text"], time.strftime("%H:%M:%S")]

    if message["room"] in messages:
        messages[message["room"]].append(msg_list)

        if len(messages[message["room"]]) > 100:
            messages[message["room"]].pop(0)

    else:
        messages[message["room"]] = [msg_list]

    send(msg_list, room=message["room"])


@socketio.on("update-user")
def update_user_handler(user):
    users[user["username"]] = True


@socketio.on("get-rooms")
def get_rooms_handler(data):
    emit("roomslist", {"rooms": rooms, "username": data["username"]}, broadcast=True)


@socketio.on("new-user")
def new_user_handler(new_user):

    username = new_user["data"]

    if username in users:
        return {"error": "user exists"}
    else:
        users[new_user["data"]] = True
        return users
