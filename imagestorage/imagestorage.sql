DROP DATABASE IF EXISTS imagestorage;
CREATE DATABASE imagestorage;
\c imagestorage;

DROP TABLE IF EXISTS images;
CREATE TABLE images(
    imageid SERIAL NOT NULL,
    imagename text NOT NULL default '',
    link text NOT NULL default '',
    privacy int NOT NULL default 0,
    PRIMARY KEY (imageid)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    userid serial NOT NULL,
    username text NOT NULL default '',
    password text NOT NULL default '',
    PRIMARY KEY (userid)
);

DROP TABLE IF EXISTS userimage;
CREATE TABLE userimage(
    id serial NOT NULL,
    imageid int NOT NULL default 0,
    userid int NOT NULL default 0,
    PRIMARY KEY (id),
    FOREIGN KEY (imageid) REFERENCES images (imageid),
    FOREIGN KEY (userid) REFERENCES users (userid)
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags(
    tagid serial NOT NULL,
    name text NOT NULL default '',
    PRIMARY KEY (tagid)
);

DROP TABLE IF EXISTS tagmanager;
CREATE TABLE tagmanager(
    id serial NOT NULL,
    imageid int NOT NULL default 0,
    tagid int NOT NULL default 0,
    PRIMARY KEY (id),
    FOREIGN KEY (imageid) REFERENCES images (imageid),
    FOREIGN KEY (tagid) REFERENCES tags (tagid)
);

DROP USER IF EXISTS mastermanager;

CREATE ROLE mastermanager WITH LOGIN;
ALTER USER mastermanager WITH PASSWORD 'dR7ha66feguprutha7UjebuspeTeRaja';
GRANT SELECT, INSERT ON tags, users, images, tagmanager, userimage TO mastermanager;
GRANT USAGE, SELECT ON users_userid_seq, tagmanager_id_seq, tags_tagid_seq, userimage_id_seq, images_imageid_seq TO mastermanager;

CREATE EXTENSION IF NOT EXISTS pgcrypto;