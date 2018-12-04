import sqlite3

def get_school(id=None):
    '''
    Returns a list of tuples of schools.
    If id is specified, returns a tuple for the school
    '''
    with sqlite3.connect('schools.db') as db:
        c = db.cursor()
        command = "SELECT * FROM schools"
        if (id):
            command += " WHERE schoolNumber={}".format(id)
        c.execute(command)
        if (id):
            return c.fetchone()
        else:
            return c.fetchall()
