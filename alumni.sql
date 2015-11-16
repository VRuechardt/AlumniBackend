CREATE TABLE IF NOT EXISTS users
   (id INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
    email           TEXT,
    lastname        TEXT,
    firstname       TEXT,
    password        TEXT,
    authenticated   INTEGER,
    logincode		TEXT,
    authenticationcode TEXT);

CREATE TABLE IF NOT EXISTS events
	 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		name			      TEXT,
    description     TEXT,
    startdate       INTEGER(20),
    enddate         INTEGER(20));

CREATE TABLE IF NOT EXISTS attendees
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userID          INTEGER,
    eventID         INTEGER);

CREATE TABLE IF NOT EXISTS announcements
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    eventID         INTEGER,
    userID          INTEGER,
    comment         TEXT,
    posted          INTEGER(20));