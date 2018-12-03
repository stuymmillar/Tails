import sqlite3

def validate_login(username, password):
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT username, password FROM login"
        c.execute(command)
        for user in c.fetchall():
            if username == user[0] and password == user[1]:
                return True
    return False

def register_user(username, password, re_password, schoolname, longitude, latitude):
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT username FROM login"
        for registered_username in c.execute(command):
            if username == registered_username[0]:
                return False
        command = "INSERT INTO login VALUES (?, ?, ?, ?, ?)"
        c.execute(command, (username, password, schoolname, longitude, latitude))
        return True
