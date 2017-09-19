#!/bin/env python
import os

port = int(os.environ.get('PORT', 5000)) 

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app,"0.0.0.0",port)
