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