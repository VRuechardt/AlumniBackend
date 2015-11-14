
from flask import session
import sqlite3

def restricted(func):

    def check_login(self):
        if 'email' in session:
            return func()
        return {"unauthorized": True}
    return check_login
