import sqlite3

def validate_login(username, password):
    if not (username and password):
        return (False, "Username or password missing.")
    with sqlite3.connect('users.db') as db:
        c = db.cursor()
        command = "SELECT username, password FROM login"
        c.execute(command)
        users = c.fetchall()
        for user in users:
            if username == user[0] and password == user[1]:
                return (True, "Successfully logged in!")
    return (False, "Incorrect username or password.")

def register_user(username, password, schoolname, longitude, latitude):
    
    return
