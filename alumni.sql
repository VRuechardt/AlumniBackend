
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS education;
DROP TABLE IF EXISTS experience;
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
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email           TEXT,
    lastname        TEXT,
    firstname       TEXT,
    password        TEXT,
    authenticated   INTEGER,
    logincode		    TEXT,
    street          TEXT,
    streetnumber    TEXT,
    zipcode         TEXT,
    city            TEXT,
    country         TEXT,
    officestreet          TEXT,
    officestreetnumber    TEXT,
    officezipcode         TEXT,
    officecity            TEXT,
    officecountry         TEXT,
    authenticationcode TEXT);

CREATE TABLE IF NOT EXISTS education
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fromdate        INTEGER(20),
    todate          INTEGER(20),
    title           TEXT,
    userID          INTEGER(20));

CREATE TABLE IF NOT EXISTS experience
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fromdate        INTEGER(20),
    todate          INTEGER(20),
    title           TEXT,
    userID          INTEGER(20));

CREATE TABLE IF NOT EXISTS events
	 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created         INTEGER(20),
    userID          INTEGER,
		name			      TEXT,
    description     TEXT,
    startdate       INTEGER(20),
    enddate         INTEGER(20),
    street          TEXT,
    streetnumber    TEXT,
    zipcode         TEXT,
    city            TEXT,
    country         TEXT,
    institution     TEXT);

CREATE TABLE IF NOT EXISTS attendees
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userID          INTEGER,
    eventID         INTEGER,
    state           INTEGER); -- the state indicates whether an attendee RSVPd, set a 'maybe', declined or is just invited.

CREATE TABLE IF NOT EXISTS announcements -- this might be rationalized away with the comment table
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    eventID         INTEGER,
    userID          INTEGER,
    comment         TEXT,
    posted          INTEGER(20));

CREATE TABLE IF NOT EXISTS comments
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userID          INTEGER,
    content         TEXT);
-- need to think about a way to linking comments to different segments so comments can be all the same. maybe a seperate 'post' table which all postings join to

CREATE TABLE IF NOT EXISTS messages
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    conversationID  INTEGER,
    userID          INTEGER, -- the user that sent the message
    content         TEXT,
    timestamp       INTEGER(20));

-- messages and participants are linked to this table to have a many to many relationship for both messages and message participants
CREATE TABLE IF NOT EXISTS conversations
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    topic           TEXT,
    adminID         INTEGER);

CREATE TABLE IF NOT EXISTS conversationparticipants
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    conversationID  INTEGER,
    userID          INTEGER);

-- table structure tbd
CREATE TABLE IF NOT EXISTS offers
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp       INTEGER(20));

-- table structure tbd
CREATE TABLE IF NOT EXISTS requests
   (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp       INTEGER(20));


-- adding some dummy data
INSERT INTO users (email, lastname, firstname, password) VALUES ('valentin@ruechardt.de', 'Ruechardt', 'Valentin', '0932f91eafea248b0ce8e0140c85322eee6abac2a04acd97d4c48254c0d72123');
INSERT INTO users (email, lastname, firstname, password) VALUES ('christian.brachert@web.de', 'Brachert', 'Christian', '0932f91eafea248b0ce8e0140c85322eee6abac2a04acd97d4c48254c0d72123');