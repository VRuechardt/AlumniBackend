import sqlite3
import cgi


def email_to_user_id(email):

    conn = sqlite3.connect('alumni.db')
    c = conn.cursor()
    user_email = (email,)
    c.execute('SELECT id FROM users WHERE email = ?', user_email)
    user_id = c.fetchone()[0]

    return user_id

def get_user(userID):

    conn = sqlite3.connect('alumni.db')
    c = conn.cursor()
    c.execute('SELECT id, firstname, lastname FROM users WHERE id = ?', (userID,))

    r = [dict((c.description[i][0], value) for i, value in enumerate(row)) for row in c.fetchall()]
    c.connection.close()
    return r[0] if r else None

def nl2br(string):
    s = cgi.escape(string)
    return s.replace('\n', '<br>\n')