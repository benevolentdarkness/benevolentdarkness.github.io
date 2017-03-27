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
    age int NOT NULL default 0,
    password text NOT NULL default 'password',
    PRIMARY KEY (userid)
);

DROP USER IF EXISTS sugmanager;
DROP USER IF EXISTS usermanager;
DROP USER IF EXISTS mastermanager;

CREATE ROLE sugmanager WITH LOGIN;
ALTER USER sugmanager WITH PASSWORD 'PuBuY5pRuw2YeHaBeN7pAcu2eH2nas4u';

CREATE ROLE usermanager WITH LOGIN;
ALTER USER usermanager WITH PASSWORD 'HeWudrasEnamEkEcHuqUzatrEdE3AbAp';

CREATE ROLE mastermanager WITH LOGIN;
ALTER USER mastermanager WITH PASSWORD 'dR7ha66feguprutha7UjebuspeTeRaja';

GRANT ALL ON suggestions TO sugmanager;
GRANT ALL ON users TO usermanager;
GRANT ALL ON suggestions, users TO mastermanager;
GRANT USAGE, SELECT ON SEQUENCE users_userid_seq TO usermanager;
GRANT USAGE, SELECT ON SEQUENCE suggestions_id_seq TO sugmanager;