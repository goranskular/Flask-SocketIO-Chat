#!/bin/env python
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

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

port = int(os.environ.get('PORT', 5000)) 

from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app,"0.0.0.0",port)
