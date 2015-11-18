
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS attendees;
DROP TABLE IF EXISTS announcements;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS conversationparticipants;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS requests;

CREATE TABLE IF NOT EXISTS users
   (id INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
    email           TEXT,
    lastname        TEXT,
    firstname       TEXT,
    password        TEXT,
    authenticated   INTEGER,
    logincode		    TEXT,
    authenticationcode TEXT);

CREATE TABLE IF NOT EXISTS events
	 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created         INTEGER(20),
		name			      TEXT,
    description     TEXT,
    startdate       INTEGER(20),
    enddate         INTEGER(20),
    street          TEXT,
    streetnumber    TEXT,
    zipcode         TEXT,
    institution     TEXT);

CREATE TABLE IF NOT EXISTS attendees
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userID          INTEGER,
    eventID         INTEGER,
    state           INTEGER);

CREATE TABLE IF NOT EXISTS announcements
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    eventID         INTEGER,
    userID          INTEGER,
    comment         TEXT,
    posted          INTEGER(20));

CREATE TABLE IF NOT EXISTS comments
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userID          INTEGER,
    content         TEXT);

CREATE TABLE IF NOT EXISTS messages
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    conversationID  INTEGER,
    content         TEXT,
    timestamp       INTEGER(20));

CREATE TABLE IF NOT EXISTS conversations
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    topic           TEXT,
    adminID         INTEGER);

CREATE TABLE IF NOT EXISTS conversationparticipants
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    conversationID  INTEGER,
    userID          INTEGER);

CREATE TABLE IF NOT EXISTS offers
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp       INTEGER(20));

CREATE TABLE IF NOT EXISTS requests
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp       INTEGER(20));



INSERT INTO users (email, lastname, firstname, password) VALUES ('valentin@ruechardt.de', 'Ruechardt', 'Valentin', '0932f91eafea248b0ce8e0140c85322eee6abac2a04acd97d4c48254c0d72123');
INSERT INTO users (email, lastname, firstname, password) VALUES ('christian.brachert@web.de', 'Brachert', 'Christian', '0932f91eafea248b0ce8e0140c85322eee6abac2a04acd97d4c48254c0d72123');