CREATE TABLE users
       	(id INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
       	email           TEXT,
       	lastname        TEXT,
       	firstname       TEXT,
       	password        TEXT,
       	authenticated   INTEGER,
       	logincode		TEXT,
       	authenticationcode TEXT);

CREATE TABLE events
		(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		name			TEXT)