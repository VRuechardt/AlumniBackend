import sqlite3
import cgi


def email_to_user_id(email):

    conn = sqlite3.connect('alumni.db')
    c = conn.cursor()
    user_email = (email,)
    c.execute('SELECT id FROM users WHERE email = ?', user_email)
    user_id = c.fetchone()[0]

    return user_id


def nl2br(string):
    s = cgi.escape(string)
    return s.replace('\n', '<br>\n')