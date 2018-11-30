#id_number,school_name, latitude, longitude

import json
import urllib.request
import sqlite3
import csv

DB_FILE = "schools.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

url = "https://data.cityofnewyork.us/resource/g2qs-86ey.json"
schoollist = json.loads(urllib.request.urlopen(url).read())

def generateTable():
    c.execute("CREATE TABLE schools(schoolNumber INTEGER, schoolname TEXT, longitude DECIMAL, latitude DECIMAL)")
    entryNum = 0
    for school in schoollist:
        try:
            c.execute("INSERT INTO schools({},{},{},{})".format(entryNum, school['school_name'], school['latitude'], school['longitude']))
        except:
            c.execute("INSERT INTO schools({},{},{},{})".format(entryNum, school['school_name'], school['latitude'], school['longitude']))
        entry += 1

generateTable()
#print(schoollist)
