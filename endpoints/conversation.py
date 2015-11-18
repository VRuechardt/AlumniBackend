from flask_restful import Resource, reqparse
from flask import session
import sqlite3
from decorators.auth import restricted


class conversation(Resource):
    def get(self, id):
        pass
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('participants', action='append')
        parser.add_argument('topic')
        args = parser.parse_args()
        creatorID = 'asd' #session['email']
        participantsIDs = [creator]
        for i in args['participants']:
            participantsIDs.append(i[0])
        print participantsIDs
        conn = sqlite3.connect("alumni.db")
        c = conn.cursor()
        if len(args['participants']) == 1:
            c.execute("INSERT INTO conversations (topic, adminID) VALUES (?)", (args['topic']))
        else:
            c.execute("INSERT INTO conversations (topic, adminID) VALUES (?)", (args['topic'],creatorID)
        conversationID = c.lastrowid()
        conn.commit()
        conn.close()

class conversationParticipants(Resource):
    def get(self, id):
        pass