# app.py
# Python Socket.IO chat server (Flask + Flask-SocketIO)
# Features: real-time messaging, rooms, user status, typing indicator, in-memory message history

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")
# Use eventlet or gevent for production (install eventlet)
socketio = SocketIO(app, cors_allowed_origins="*")  # default async mode: eventlet if installed

# In-memory stores (demo only)
USERS = {}      # sid -> {"username": str, "room": str}
ONLINE = {}     # username -> sid
ROOM_MESSAGES = {}  # room -> [ {username, text, ts} ]

DEFAULT_ROOM = "global"

# Utility
def now_ts():
    return datetime.utcnow().isoformat() + "Z"

# Routes
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

# Socket.IO events
@socketio.on("connect")
def handle_connect():
    print("Client connected",)
    emit("connected", {"msg": "connected", "ts": now_ts()})

@socketio.on("set_username")
def handle_set_username(data):
    """
    data = {"username": "Alice", "room": "global"}  # room optional
    """
    sid = request_sid = getattr(socketio, "server", None)  # not used; use flask-socketio context
    username = (data.get("username") or "").strip()
    room = data.get("room") or DEFAULT_ROOM
    if not username:
        emit("error", {"msg": "Missing username."})
        return

    # Save mapping
    USERS[request.sid] = {"username": username, "room": room}
    ONLINE[username] = request.sid

    join_room(room)
    # Ensure room exists
    ROOM_MESSAGES.setdefault(room, [])

    # Notify client with existing users & messages
    emit("login_success", {
        "username": username,
        "room": room,
        "users": list(ONLINE.keys()),
        "messages": ROOM_MESSAGES[room]
    })

    # Broadcast presence change
    emit("user_joined", {"username": username, "ts": now_ts()}, broadcast=True)
    print(f"{username} joined room {room}")

@socketio.on("join_room")
def handle_join_room(data):
    """
    data = {"room": "roomName"}
    """
    room = data.get("room") or DEFAULT_ROOM
    user = USERS.get(request.sid)
    if not user:
        emit("error", {"msg": "Not logged in."})
        return

    prev_room = user["room"]
    if prev_room == room:
        emit("joined_room", {"room": room})
        return

    leave_room(prev_room)
    join_room(room)
    user["room"] = room
    ROOM_MESSAGES.setdefault(room, [])
    emit("joined_room", {"room": room})
    emit("user_changed_room", {"username": user["username"], "room": room}, broadcast=True)

@socketio.on("send_message")
def handle_send_message(data):
    """
    data = {"text": "hello"}
    """
    text = (data.get("text") or "").strip()
    if not text:
        return

    user = USERS.get(request.sid)
    if not user:
        emit("error", {"msg": "Not logged in."})
        return

    room = user["room"]
    username = user["username"]
    message = {"username": username, "text": text, "ts": now_ts()}
    # save history (cap to last 200)
    ROOM_MESSAGES.setdefault(room, []).append(message)
    if len(ROOM_MESSAGES[room]) > 200:
        ROOM_MESSAGES[room] = ROOM_MESSAGES[room][-200:]

    # Broadcast to room
    emit("new_message", message, to=room)
    print(f"[{room}] {username}: {text}")

@socketio.on("typing")
def handle_typing(data):
    """
    data = {"typing": True/False}
    Broadcasts typing status to other users in room.
    """
    typing = bool(data.get("typing"))
    user = USERS.get(request.sid)
    if not user:
        return
    room = user["room"]
    emit("user_typing", {"username": user["username"], "typing": typing}, room=room, include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    user = USERS.pop(request.sid, None)
    if user:
        username = user["username"]
        ONLINE.pop(username, None)
        emit("user_left", {"username": username, "ts": now_ts()}, broadcast=True)
        print(f"{username} disconnected")
    else:
        print("Unknown client disconnected")

if __name__ == "__main__":
    # For local dev: install eventlet and run
    # pip install flask flask-socketio eventlet
    # python app.py
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
