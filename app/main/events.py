from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from datetime import datetime
import pytz

cest = pytz.timezone('Europe/Zagreb')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

messages = {}

def addhistory(room,message):
    if room in messages:
        if len(messages[room])>10:
            messages[room].pop(0)
        messages[room].append(message)
    else:
        messages[room] = [message]


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

