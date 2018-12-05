# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee  

import os
import json
import urllib

from flask import Flask, request, session, redirect, render_template, flash

from util.manage_user import register_user, validate_login
from util.schools import get_school

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/')
def home():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    return render_template("home.html", user=session["user"])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "loggedin" in session:
        return redirect('/')
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            flash("Username or password missing.", 'alert')
            return render_template("login.html")
        if validate_login(username, password):
            flash("Successfully logged in as {}".format(username), 'success')
            session["loggedin"] = True
            session["user"]=username
            return redirect('/')
        else:
            flash("Incorrect username or password.", 'alert')
            return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    school_data = get_school()
    school_data.sort(key=lambda tup:tup[1]) # sort by school name
    if request.method == 'GET':
        return render_template("register.html",
                                schools=school_data)
    else:
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']
        school_id = request.form['school_id']
        school_info = get_school(id=school_id)
        longitude = school_info[2]
        latitude = school_info[3]
        if not (username and password and re_password
                and school_id and longitude and latitude):
            flash("One or more fields missing.", 'alert')
            return redirect('register')
        if password != re_password:
            flash("Passwords do not match.", 'alert')
            return redirect('register')
        success = register_user(username, password, password,
                                school_id, longitude, latitude)
        if success:
            flash("Registered {}".format(username), 'success')
            return redirect('login')
        else:
            flash("Username {} already exists.".format(username), 'alert')
            return redirect('register')

@app.route('/news')
def story():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    url_stub="http://api.nytimes.com/svc/topstories/v2/home.json?api-key="
    with open('keys.json') as f:
        key = json.load(f)["news"]
    req=urllib.request.urlopen(url_stub+key)
    fin=json.loads(req.read())

    return render_template("news.html",
                               news=fin["results"])

'''
@app.route("/transit")
def transit():
    data = json.loads((urllib.request.urlopen("https://www.mapquestapi.com/traffic/v2/incidents?&outFormat=json&boundingBox=40.790419549617724%2C-73.8229751586914%2C40.635840993386466%2C-74.19136047363281&key=3ajPJ1Wrf9x12UgvIzWGIvhUCdpdxacq")).read())
    incidents = []
    print(data["incidents"][5]["shortDesc"])
    for x in range(0,5):
        incidents.append(data["incidents"][x]["shortDesc"])
    schooldata = json.loads((urllib.request.urlopen("https://data.cityofnewyork.us/resource/g2qs-86ey.json")).read())
    print(schooldata[140])
    
    homelat = 40.775088
    homelong = -73.977815
    #schoollat = 40.71759                                                      
    #schoollong = -74.013748                                                   
    schoollat = schooldata[140]["latitude"]
    schoollong = schooldata[140]["longitude"]
    url = "https://transit.api.here.com/v3/route.json?app_id=7jNm9uNlO3Up0edHuqK0&app_code=6QxzobcNH0yyWBd27YItEg&routing=all&dep=" + str(homelat) + "," + str(homelong) + "&arr=" + str(schoollat) + "," + str(schoollong) + "&time=2018-11-27T07%3A30%3A00"
    data = json.loads((urllib.request.urlopen(url)).read())
    stations = []
    for x in range(1, (len(data["Res"]["Connections"]["Connection"]) - 1)):
        stations.append(str("The " + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Dep"]["Transport"]["name"]) + " from " + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Dep"]["Stn"]["name"]) + " to " + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Arr"]["Stn"]["name"])))
    return str(incidents) + str(stations)
'''


app.debug=True
app.run()
