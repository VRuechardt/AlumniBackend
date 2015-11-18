from flask_restful import Resource, reqparse
from flask import session
from util import stuff
import sqlite3
from decorators.auth import restricted


class conversation(Resource):
    @restricted
    def get(self):
        creatorID = stuff.email_to_user_id(session['email'])
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()
        c.execute("SELECT conversationID FROM conversationparticipants WHERE userID = ?", (creatorID,))

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]

        for i in r:
            i['conversation'] = stuff.get_conversation(int(i['conversationID']))
        c.connection.close()
        return r

    @restricted
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('participants', action='append')
        parser.add_argument('topic')
        args = parser.parse_args()
        creatorID = stuff.email_to_user_id(session['email'])
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()
        if len(args['participants']) == 1:
            c.execute("INSERT INTO conversations (topic) VALUES (?)", (args['topic'],))
        else:
            c.execute("INSERT INTO conversations (topic, adminID) VALUES (?, ?)", (args['topic'],creatorID))
        conversationID = c.lastrowid
        for p in args['participants']:
            c.execute("INSERT INTO conversationparticipants (conversationID, userID) VALUES (?, ?)", (conversationID, stuff.email_to_user_id(p)))
        c.execute("INSERT INTO conversationparticipants (conversationID, userID) VALUES (?, ?)", (conversationID, creatorID))
        conn.commit()
        conn.close()
        return conversationID

class AddUser(Resource):
    @restricted
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user')
        parser.add_argument('conversation')
        args = parser.parse_args()
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()
        r = c.execute("SELECT userID FROM conversationparticipants WHERE conversationID = ?", (args['conversation'])).fetchall()
        if stuff.email_to_user_id(session['email']) in (v[0] for v in enumerate(r)):
            c.execute('INSERT INTO conversationparticipants (userID, conversationID) VALUES (?, ?)', (stuff.email_to_user_id(args['user']), args['conversation']))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return {"unauthorized": True}, 401
        return 200

class conversationParticipants(Resource):
    @restricted
    def get(self, id):
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()
        c.execute("SELECT userID FROM conversationparticipants WHERE conversationID = ?", (id,))
        c.execute("SELECT userID FROM conversationparticipants WHERE conversationID = ?", (id,))
        r = c.fetchall()
        if stuff.email_to_user_id(session['email']) in [v[0] for i, v in enumerate(r)]:
            return [v[0] for i, v in enumerate(r)]
        else:
            return {"unauthorized": True}, 401

class Message(Resource):
    @restricted
    def get(self, conv_id, start_id):
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()

        if start_id == 0:
            data = (conv_id,)
            c.execute("SELECT * FROM messages WHERE conversationID = ? ORDER BY id DESC LIMIT 20", data)
        else:
            data = (conv_id, start_id)
            c.execute("SELECT * FROM messages WHERE conversationID = ? AND id < ? ORDER BY id DESC LIMIT 20", data)

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r