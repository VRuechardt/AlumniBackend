
from flask_restful import Resource, reqparse
import sqlite3
from decorators.auth import restricted
from util import stuff
import json


class Event(Resource):

    @restricted
    def get(self, event_id):
        conn = sqlite3.connect('alumni.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        id = (int(event_id),)
        c.execute('SELECT * FROM events WHERE id = ?', id)

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r[0] if r else None


class Events(Resource):

    @restricted
    def get(self):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        c.execute('SELECT * FROM events')

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r


    @restricted
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('startdate')
        parser.add_argument('enddate')
        parser.add_argument('description')
        args = parser.parse_args()

        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        c.execute("INSERT INTO events (name, description, startdate, enddate) VALUES (?, ?, ?, ?)", (args['name'], stuff.nl2br(args['description']), args['startdate'], args['enddate']))

        id = (int(c.lastrowid),)
        c.execute('SELECT * FROM events WHERE id = ?', id)
        conn.commit()

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r[0] if r else None
