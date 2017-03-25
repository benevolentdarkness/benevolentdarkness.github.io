DROP DATABASE IF EXISTS chicken;

CREATE DATABASE chicken;
\c chicken;

DROP TABLE IF EXISTS suggestions;
CREATE TABLE suggestions (
    ID serial NOT NULL,
    Firstname varchar(35) NOT NULL default '',
    Lastname varchar(35) NOT NULL default '',
    age int NOT NULL default 0,
    suggestiontype varchar(35) NOT NULL default '',
    suggestion text NOT NULL default '',
    votes int NOT NULL default 0,
    PRIMARY KEY (ID)
);