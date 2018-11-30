from flask import Flask, render_template
import json
from urllib import request

app = Flask(__name__)

@app.route('/')
def render_test():
    schooldata = json.loads((request.urlopen("https://data.cityofnewyork.us/resource/g2qs-86ey.json")).read())
    #print(schooldata[0])
    homelat = 40.775088
    homelong = -73.977815
    #schoollat = 40.71759
    #schoollong = -74.013748
    schoollat = schooldata[0]["latitude"]
    schoollong = schooldata[0]["longitude"]
    url = "https://transit.api.here.com/v3/route.json?app_id=7jNm9uNlO3Up0edHuqK0&app_code=6QxzobcNH0yyWBd27YItEg&routing=all&dep=" + str(homelat) + "," + str(homelong) + "&arr=" + str(schoollat) + "," + str(schoollong) + "&time=2018-11-27T07%3A30%3A00"
    data = json.loads((request.urlopen(url)).read())
    #return str(data["Res"]["Connections"]["Connection"][1]["Sections"]["Sec"][0]["Arr"]["Stn"]["name"]) + " to " + str(data["Res"]["Connections"]["Connection"][1]["Sections"]["Sec"][len(data["Res"]["Connections"]["Connection"][1]["Sections"]["Sec"]) - 1]["Dep"]["Stn"]["name"] + ", School: " + schooldata[0]["school_name"])
    return str(data["Res"]["Connections"]["Connection"][0])


if __name__ == '__main__':
    app.debug = True
    app.run()

