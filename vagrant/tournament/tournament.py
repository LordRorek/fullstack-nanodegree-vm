#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import random
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = connect()
    c = db.cursor()
    c.execute("UPDATE swiss SET points = 0 WHERE ID > 0;")
    c.execute("UPDATE swiss SET matches = 0 WHERE ID > 0;")
    c.execute("UPDATE swiss SET opid = null WHERE ID > 0;")
    c.execute("UPDATE swiss SET OMW = 0 WHERE ID > 0;")
    db.commit()
    db.close()    

def deletePlayers():
    db = connect()
    c = db.cursor()
    c.execute("TRUNCATE TABLE swiss;")
    db.commit()
    db.close()

def countPlayers():
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(ID) FROM swiss TBL;")
    result = c.fetchall()[0][0]
    db.commit()
    db.close()
    if result == None:
        return 0
    else:
        return result

def registerPlayer(name):
    db = connect()
    c = db.cursor()
    c.execute("INSERT into swiss (name, points, matches, OMW) VALUES (%s, %s, %s, %s);", (name, 0, 0, 0));
    db.commit()
    db.close()

def OMW_ranking():
    db = connect()
    c = db.cursor()
    c.execute("SELECT id FROM swiss TBL ORDER BY id ASC;")
    id_list = c.fetchall()
    for p in id_list:
        c.execute("UPDATE swiss SET OMW = 0 WHERE ID = %s;", ([p[0]]));   
    for n in id_list:
        c.execute("SELECT opid FROM swiss WHERE ID = %s;", ([n[0]]));
        opid_list = c.fetchall()[0][0]
        for m in opid_list:
            c.execute("SELECT points FROM swiss WHERE ID = %s;", ([m]));
            score = c.fetchall()[0][0]
            c.execute("SELECT OMW FROM swiss WHERE ID = %s;",([n[0]]));
            points = c.fetchall()[0][0]
            c.execute("UPDATE swiss SET OMW = %s + %s WHERE ID = %s;", (points, score, n[0]));
    db.commit()
    db.close()
        

    

def playerStandings():
    db = connect()
    c = db.cursor()
    OMW_ranking()
    c.execute("SELECT id, name, points, matches FROM swiss TBL ORDER BY points DESC, OMW DESC;")
    result = c.fetchall()
    db.close()
    return result

def reportMatch(player1, player2):
    db = connect()
    c = db.cursor()
    match = random.randrange(0, 4, 1)
    if match == 1:#Player 1 wins
        c.execute("UPDATE swiss SET opid = opid || (%s) , points = (points + 3), matches = (matches + 1) WHERE ID = %s;", ([player2], player1));
        c.execute("UPDATE swiss SET opid = opid || (%s), matches = (matches + 1) WHERE ID = %s;", ([player1], player2));
    if match == 2:#Player 2 wins
        c.execute("UPDATE swiss SET opid = opid || (%s) , points = (points + 3), matches = (matches + 1) WHERE ID = %s;", ([player1], player2));
        c.execute("UPDATE swiss SET opid = opid || (%s), matches = (matches + 1) WHERE ID = %s;", ([player2], player1));
    if match == 3:#The match is a draw
        c.execute("UPDATE swiss SET opid = opid || (%s) , points = (points + 1), matches = (matches + 1) WHERE ID = %s;", ([player2], player1));
        c.execute("UPDATE swiss SET opid = opid || (%s), matches = (matches + 1) WHERE ID = %s;", ([player1], player2));
        c.execute("UPDATE swiss SET opid = opid || (%s) , points = (points + 1), matches = (matches + 1) WHERE ID = %s;", ([player1], player2));
        c.execute("UPDATE swiss SET opid = opid || (%s), matches = (matches + 1) WHERE ID = %s;", ([player2], player1));    
    db.commit()
    db.close()
                            
def swissPairings():
    db = connect()
    c = db.cursor()
    rank = playerStandings()
    tup1 = ()
    pairs = []
    for p in rank:
        tup1 = tup1 + p[0:2]
        if len(tup1) > 2:
            pairs.append(tup1)
            tup1 = ()
    return pairs

