
from flask import session
import sqlite3

def restricted(func):

    def check_login(self):
        if 'email' in session:
            return func(self)
        return {"unauthorized": True}
    return check_login
