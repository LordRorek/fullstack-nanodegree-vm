-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
CREATE TABLE swiss (id SERIAL, name TEXT, points INTEGER, matches INTEGER, opid INTEGER[], OMW INTEGER,  PRIMARY KEY (id));
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
