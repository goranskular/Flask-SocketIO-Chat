#!/bin/env python
import os
ON_HEROKU = os.environ.get('ON_HEROKU')

if ON_HEROKU:
    port = int(os.environ.get('PORT', 17995)) 
else:
    port = 17995

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app,"0.0.0.0",port)
