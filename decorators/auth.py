
from flask import session
import sqlite3

def restricted(func):

    def check_login(*args, **kwargs):
        if 'email' in session:
            return func(*args, **kwargs)
        return {"unauthorized": True}
    return check_login
