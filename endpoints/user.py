from flask import session, redirect, url_for, request
from flask_restful import Resource, Api, reqparse
import hashlib
import sqlite3
import random
import util
from util import stuff
import os
from decorators.auth import restricted, restricted_myself
from werkzeug import utils
from PIL import Image

UPLOAD_FOLDER = '../Alumni/app/profile_pictures/'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_extension(filename):
    return filename.rsplit('.', 1)[1]

class CheckLogin(Resource):
    @restricted
    def get(self):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        email = (str(session['email']),)
        c.execute('SELECT * FROM users WHERE email = ?', email)
        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r[0] if r else None

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
        print res
        if len(res) > 0:
            session['email'] = args['email']
            allowedChars = 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            code = ""
            for i in range(5):
                code += random.choice(allowedChars)
            conn = sqlite3.connect('alumni.db')
            c = conn.cursor()
            c.execute('UPDATE users SET logincode = ? WHERE email = ?', (code, args['email']))
            conn.commit()
            print code
            return code, 201

        return 403

class Logout(Resource):
    @restricted
    def get(self):
        session.pop('email', None)
        return 201

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
        code = random.randint(0, 10000)
        util.mail_service.send_registration_confirmation(args['email'], code)
        c.execute("INSERT INTO USERS (email, authenticated, authenticationcode) VALUES (?,?,?)", (args['email'], 0, code))
        conn.commit()
        print(args)
        return 201


class SingleUsers(Resource):

    # get some users profile
    @restricted
    def get(self, user_id):

        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()

        id = (int(user_id),)
        c.execute('SELECT * FROM users WHERE id = ?', id)

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r[0] if r else None

    # update own profile (critical info , requires password)
    @restricted
    def put(self, user_id):
        @restricted_myself('users', 'id', user_id)
        def do_put():

            user_id = util.stuff.email_to_user_id(session['email'])

            conn = sqlite3.connect('alumni.db')
            c = conn.cursor()
            parser = reqparse.RequestParser()
            parser.add_argument('firstname', required=True)
            parser.add_argument('lastname', required=True)
            # only if user wants to change his password
            parser.add_argument('password')
            parser.add_argument('newpassword')
            args = parser.parse_args()

            if args['password'] and args['newpassword']:
                password = hashlib.sha256(args['password']).hexdigest()
                new_password = hashlib.sha256(args['newpassword']).hexdigest()

                test_data = (user_id, password)
                c.execute('SELECT * FROM users WHERE id = ? AND password = ?', test_data)
                if c.fetchall().__len__() == 0:
                    return {}, 401

                data = (args['firstname'], args['lastname'], new_password, int(user_id), password)
                c.execute('UPDATE users SET firstname = ?, lastname = ?, password = ? WHERE id = ? AND password = ?', data)
                conn.commit()
            else:
                data = (args['firstname'], args['lastname'], int(user_id))
                print data
                c.execute('UPDATE users SET firstname = ?, lastname = ? WHERE id = ?', data)
                conn.commit()
            return {}

        return do_put()




class Users(Resource):
    @restricted
    def get(self):
        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users')

        r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
        c.connection.close()
        return r

class Upload(Resource):

    @restricted
    def post(self):

        conn = sqlite3.connect('alumni.db')
        c = conn.cursor()
        email = (str(session['email']),)
        c.execute('SELECT * FROM users WHERE email = ?', email)
        res = c.fetchone()

        file = request.files['picture']
        if file and allowed_file(file.filename):
            filename = utils.secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, str(res[0]) + '.' + get_extension(filename)))
            im = Image.open(os.path.join(UPLOAD_FOLDER, str(res[0]) + '.' + get_extension(filename)))
            im.save(os.path.join(UPLOAD_FOLDER, str(res[0]) + '.png'))
            return {}, 201
        return {}, 500
