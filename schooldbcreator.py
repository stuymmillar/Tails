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
    c.execute("CREATE TABLE schools(schoolNumber INTEGER, schoolname TEXT, latitude DECIMAL, longitude DECIMAL)")# , statement TEXT)")
    for school in schoollist:
        entryNum = 0
        command = 'INSERT INTO schools VALUES({0},"{1}",{2},{3})'.format(entryNum, school['school_name'], school['latitude'], school['longitude'])#, school['overview_paragraph'])
        c.execute(command)
        entryNum += 1

generateTable()

db.commit()
db.close()
