import sqlite3
import csv

DB_FILE="users.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

def resetTable():
    try:
        c.execute("DROP TABLE login")
        c.execute("CREATE TABLE login(username TEXT PRIMARY KEY, password TEXT, schoolNumber INTEGER, latitude DECIMAL, longitude DECIMAL)")
        c.execute("INSERT INTO login VALUES('test', 'test', 274, 40.741895, -73.989308)")
    except:
        c.execute("CREATE TABLE login(username TEXT PRIMARY KEY, password TEXT, schoolNumber INTEGER, latitude DECIMAL, longitude DECIMAL)")
        c.execute("INSERT INTO login VALUES('test', 'test', 274, 40.741895, -73.989308)")

def readFrom():
    c.execute("SELECT * FROM login")
    print(c.fetchall())

resetTable()
readFrom()

db.commit()
db.close()
