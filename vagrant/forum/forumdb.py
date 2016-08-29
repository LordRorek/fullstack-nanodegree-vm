#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Get posts from database.
def GetAllPosts():
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("UPDATE posts SET content = 'cheese' WHERE content LIKE '%spam%';")
    c.execute("DELETE FROM posts WHERE content LIKE 'cheese';")
    c.execute("SELECT time, content FROM posts ORDER BY time DESC;")
    posts = ({'content': str(row[1]), 'time': str(row[0])} for row in c.fetchall())
    db.commit()
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("UPDATE posts SET content = 'cheese' WHERE content LIKE '%spam%';")
    c.execute("DELETE FROM posts WHERE content LIKE 'cheese';")
    c.execute("INSERT into posts (content) VALUES (%s);", (bleach.clean(content, strip=True),));
    db.commit()
    db.close()
    
    
