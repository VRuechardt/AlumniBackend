from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from util.mail_service import mail
from passlib.hash import sha256_crypt
import util
import sqlite3
import random

app = Flask(__name__)
CORS(app)
api = Api(app)


app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='find.my.alumnis@gmail.com',
    MAIL_PASSWORD='7p3xX9!4-o',
    MAIL_DEFAULT_SENDER=('Alumni', 'find.my.alumnis@gmail.com'))


mail.init_app(app)

class HelloWorld(Resource):
    def get(self):


        return {'hello': 'world'}
    def post(self):
        return {'hello': 'vau'}


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()

        conn =  sqlite3.connect('alumni.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (args['email'], args['password']))
        res = c.fetchall()

        if len(res) > 0:
            return 201

        return 403


class User(Resource):
    def put(self):
        conn =  sqlite3.connect('alumni.db')
        c = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('lastname')
        parser.add_argument('firstname')
        parser.add_argument('password')
        parser.add_argument('code')
        args = parser.parse_args()
        c.execute('UPDATE users SET lastname = ?, firstname = ?, password = ?, authenticated = 1 WHERE authenticationcode = ?', (args['lastname'], args['firstname'], args['password'], str(args['code'])))
        conn.commit()
        print(args)
        return 201

    def post(self):
        conn =  sqlite3.connect('alumni.db')
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

api.add_resource(HelloWorld, '/api/')
api.add_resource(User, '/api/user')
api.add_resource(Login, '/api/login')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def server_static(path):
    print '../Alumni/app/', path
    return send_from_directory('../Alumni/app/', path)


print __name__

if __name__ == '__main__':
    app.run()
