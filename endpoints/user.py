from flask import session, redirect, url_for
from flask_restful import Resource, Api, reqparse
import hashlib
import sqlite3
import random
import util
from decorators.auth import restricted


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()

        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()

        password = str(hashlib.sha256(args['password']).hexdigest())
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (args['email'], password))
        res = c.fetchall()

        if len(res) > 0:
            session['email'] = args['email']
            return 201

        return 403

class Logout(Resource):
    @restricted
    def get(self):
        session.pop('email', None)
        return 200

class User(Resource):
    def put(self):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('lastname')
        parser.add_argument('firstname')
        parser.add_argument('password')
        parser.add_argument('code')
        args = parser.parse_args()
        c.execute('UPDATE users SET lastname = ?, firstname = ?, password = ?, authenticated = 1 WHERE authenticationcode = ?', (args['lastname'], args['firstname'], hashlib.sha256(args['password']).hexdigest(), str(args['code'])))
        conn.commit()
        return 201

    @restricted
    def post(self):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        args = parser.parse_args()
        code=random.randint(0,10000)
        util.mail_service.send_registration_confirmation(args['email'], code)
        c.execute("INSERT INTO USERS (email, authenticated, authenticationcode) VALUES (?,?,?)", (args['email'], 0, code))
        conn.commit()
        print(args)
        return 201