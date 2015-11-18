
from flask import session
from flask_restful import Resource, reqparse
import sqlite3
from decorators.auth import restricted
from util import stuff
import time
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
        data = (int(round(time.time() * 1000)), stuff.email_to_user_id(session['email']), args['name'], stuff.nl2br(args['description']), args['startdate'], args['enddate'])
        c.execute("INSERT INTO events (created, userID, name, description, startdate, enddate) VALUES (?, ?, ?, ?, ?, ?)", data)

        id = (int(c.lastrowid),)
        c.execute('SELECT * FROM events WHERE id = ?', id)
        conn.commit()

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r[0] if r else None

class Attend(Resource):

    @restricted
    def get(self, event_id):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()

        user_id = stuff.email_to_user_id(session['email'])
        data = (event_id, user_id)
        c.execute("SELECT state FROM attendees WHERE eventID = ? AND userID = ?", data)
        res = c.fetchall()

        if res.__len__() == 0:
            return {}, 404
        return {'state': res[0]}, 200

    @restricted
    def put(self, event_id):
        parser = reqparse.RequestParser()
        parser.add_argument('state')
        args = parser.parse_args()
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()

        user_id = stuff.email_to_user_id(session['email'])
        data = (event_id, user_id)
        c.execute("SELECT * FROM attendees WHERE eventID = ? AND userID = ?", data)
        conn.commit()
        data = (args['state'], event_id, user_id)
        if c.fetchall().__len__() == 0:
            c.execute("INSERT INTO attendees (state, eventID, userID) VALUES (?, ?, ?)", data)
            conn.commit()
        else:
            c.execute("UPDATE attendees SET state = ? WHERE eventID = ? AND userID = ?", data)
            conn.commit()

        return {}

class Posts(Resource):

    @restricted
    def get(self, event_id):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()

        data = (event_id,)
        c.execute("SELECT * FROM announcements WHERE eventID = ? ORDER BY id DESC", data)

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]

        for i in r:
            i['user'] = stuff.get_user(i['userID'])

        return r, 200

    @restricted
    def post(self, event_id):
        parser = reqparse.RequestParser()
        parser.add_argument('comment')
        args = parser.parse_args()
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        user_id = stuff.email_to_user_id(session['email'])

        data = (event_id, user_id, args['comment'], int(round(time.time() * 1000)))
        c.execute("INSERT INTO announcements (eventID, userID, comment, posted) VALUES (?, ?, ?, ?)", data)
        conn.commit()

        print data

        return {}, 200
