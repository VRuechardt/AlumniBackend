
from flask import session
import sqlite3
from inspect import getcallargs

def restricted(func):

    def check_login(*args, **kwargs):
        if 'email' in session:
            return func(*args, **kwargs)
        return {"unauthorized": True}, 401
    return check_login

def restricted_myself(table, columnname, entry):

    def decorator(func):

        def check_myself(*args, **kwargs):

            if 'email' in session:

                conn = sqlite3.connect('alumni.db')
                c = conn.cursor()

                user_email = (session['email'],)
                c.execute('SELECT id FROM users WHERE email = ?', user_email)
                user_id = c.fetchone()[0]

                ids = (user_id, entry)
                c.execute('SELECT * FROM ' + table + ' WHERE id = ? AND ' + columnname + ' = ?', ids)
                res = c.fetchall()

                if res.__len__() == 1:
                    return func(*args, **kwargs)

            return {"unauthorized": True}, 401

        return check_myself
    return decorator
