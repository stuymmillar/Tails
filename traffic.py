from flask import Flask, render_template
import json
from urllib import request

app = Flask(__name__)

@app.route('/')
def render_test():
    url="https://www.mapquestapi.com/traffic/v2/incidents?&outFormat=json&boundingBox=40.790419549617724%2C-73.8229751586914%2C40.635840993386466%2C-74.19136047363281&key="
    with open('keys.json') as f:
        key = json.load(f)["traffic"]
    url += key
    data = json.loads((request.urlopen(url)).read())
    incidents = []
    print(data["incidents"][5]["shortDesc"])
    for x in range(0,5):
        incidents.append(data["incidents"][x]["shortDesc"])
    return str(incidents)

if __name__ == '__main__':
    app.debug = True
    app.run()
