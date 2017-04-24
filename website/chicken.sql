DROP DATABASE IF EXISTS chicken;

CREATE DATABASE chicken;
\c chicken;

DROP TABLE IF EXISTS suggestions;
CREATE TABLE suggestions (
    ID serial NOT NULL,
    userid int NOT NULL default 0,
    suggestiontype varchar(35) NOT NULL default '',
    suggestion text NOT NULL default '',
    votes int NOT NULL default 0,
    PRIMARY KEY (ID)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    userid serial NOT NULL,
    firstname varchar(35) NOT NULL default '',
    lastname varchar(35) NOT NULL default '',
    username varchar(35) NOT NULL default '',
    email text NOT NULL default '',
    password text NOT NULL default 'password',
    PRIMARY KEY (userid)
);

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id serial NOT NULL,
    userid int NOT NULL default 0,
    message TEXT NOT NULL default '',
    PRIMARY KEY (id)
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users (firstname, lastname, username, email, password)
VALUES ('Jonathan', 'Erickson', 'ChickenGoddess', 'benevolentdarkness@gmail.com', crypt('Ibanez24', gen_salt('bf')));

DROP USER IF EXISTS messagemanager;
DROP USER IF EXISTS sugmanager;
DROP USER IF EXISTS usermanager;
DROP USER IF EXISTS mastermanager;

CREATE ROLE messagemanager WITH LOGIN;
ALTER USER messagemanager WITH PASSWORD 'XyshenSsintk343b5h3bn9ndjsuz9s76aISneksI';

CREATE ROLE sugmanager WITH LOGIN;
ALTER USER sugmanager WITH PASSWORD 'PuBuY5pRuw2YeHaBeN7pAcu2eH2nas4u';

CREATE ROLE usermanager WITH LOGIN;
ALTER USER usermanager WITH PASSWORD 'HeWudrasEnamEkEcHuqUzatrEdE3AbAp';

CREATE ROLE mastermanager WITH LOGIN;
ALTER USER mastermanager WITH PASSWORD 'dR7ha66feguprutha7UjebuspeTeRaja';

GRANT SELECT, INSERT ON messages TO messagemanager;
GRANT SELECT, INSERT ON suggestions TO sugmanager;
GRANT SELECT, INSERT ON users TO usermanager;
GRANT SELECT, INSERT ON suggestions, users, messages TO mastermanager;
GRANT USAGE, SELECT ON SEQUENCE users_userid_seq TO usermanager;
GRANT USAGE, SELECT ON SEQUENCE suggestions_id_seq TO sugmanager;
GRANT USAGE, SELECT ON SEQUENCE messages_id_seq TO messagemanager;
GRANT USAGE, SELECT ON SEQUENCE messages_id_seq TO mastermanager;