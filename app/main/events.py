from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from datetime import datetime
import pytz

import os
import psycopg2
import urllib.parse
import pickle

def save():
    cur.execute("DELETE FROM rooms WHERE room = 'ALL';")
    cur.execute("INSERT INTO rooms (room, messages) VALUES (%s, %s)", ("ALL", pickle.dumps(messages))))
    conn.commit()

def load():
    cur.execute("SELECT messages FROM rooms WHERE room='ALL';")
    res = cur.fetchone()
    if res:
        messages=pickle.loadsres[0])

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

messages = {}
load()

cest = pytz.timezone('Europe/Zagreb')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

def addhistory(room,message):
    if room in messages:
        if len(messages[room])>10:
            messages[room].pop(0)
        messages[room].append(message)
    else:
        messages[room] = [message]
    save()


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    for m in messages[room]:
        emit('message', {'msg': 'HISTORY:' + m}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    m = cest.localize(datetime.now()).strftime(fmt)+': '+session.get('name')+':'+message['msg']
#    m = session.get('name')+':'+message['msg']
    emit('message', {'msg': m}, room=room)
    addhistory(room,m)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

