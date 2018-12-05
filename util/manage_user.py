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

def register_user(username, password, re_password,
        school_id, longitude, latitude):
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT username FROM login"
        for registered_username in c.execute(command):
            if username == registered_username[0]:
                return False
        command = "INSERT INTO login VALUES (?, ?, ?, ?, ?)"
        c.execute(command, (username, password, school_id, longitude, latitude))
        return True


def getSchoolID(username):
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT schoolNumber FROM login WHERE username = " + "'" + username + "'"
        c.execute(command)
        return c.fetchall()[0][0]

# print(getSchoolID("test"))

def getSchoolLocation(username):
    with sqlite3.connect('schools.db') as db:
        c = db.cursor()
        command = "SELECT latitude,longitude FROM schools WHERE schoolNumber = " + str(getSchoolID(username))
        c.execute(command)
        return c.fetchall()[0]

# getSchoolLocation("test")

def getSchoolStatement(username):
    with sqlite3.connect('schools.db') as db:
        c = db.cursor()
        command = "SELECT statement FROM schools WHERE schoolNumber = " + str(getSchoolID(username))
        c.execute(command)
        return c.fetchall()[0][0]

# print(getSchoolStatement("test"))

def getUserLocation(username):
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT latitude,longitude FROM login WHERE username = " + "'" + username + "'"
        c.execute(command)
        return c.fetchall()[0]
#print(getUserLocation("test"))
