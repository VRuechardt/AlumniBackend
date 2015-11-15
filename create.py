import hashlib
import sqlite3

conn = sqlite3.connect('alumni.db')
c = conn.cursor()
lastname = "Ruechardt"
firstname = "Valentin"
email = "valentin@ruechardt.de"
password = hashlib.sha256("schokolade").hexdigest()
c.execute('INSERT INTO users (email, lastname, firstname, password) VALUES (?, ?, ?, ?)', (email, lastname, firstname, password))
conn.commit()