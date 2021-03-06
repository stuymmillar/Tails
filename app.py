# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee

import os
import json
import urllib

from flask import Flask, request, session, redirect, render_template, flash
import sqlite3

from util.schooldbcreator import generateTable
from util.manage_user import register_user, validate_login, getSchoolLocation, getSchoolStatement, getSchoolName, getUserLocation
from util.schools import get_school

app = Flask(__name__)
app.secret_key = os.urandom(64)

generateTable()

@app.route('/')
def home():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    return render_template("home.html", user=session["user"],
                           School = getSchoolName(session["user"]),
                           SchoolInfo = getSchoolStatement(session["user"]))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "loggedin" in session:
        flash("You are already logged in", 'alert')
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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if "loggedin" in session:
        session.pop("loggedin")
        session.pop("user")
        flash("Goodbye!", 'success')
        return redirect('/login')
    else:
        flash("You are not logged in.", 'alert')
        return redirect('/login')

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
        try:
            url = "https://ipapi.co/json"
            req = urllib.request.urlopen(url)
            data = json.loads(req.read())
            latitude = data["latitude"]
            longitude = data["longitude"]
        except:
            flash("API Error")
            return redirect("register")
        if not (username and password and re_password
                and school_id and longitude and latitude):
            flash("One or more fields missing.", 'alert')
            return redirect('register')
        if password != re_password:
            flash("Passwords do not match.", 'alert')
            return redirect('register')
        success = register_user(username, password, password,
                                school_id, latitude, longitude)
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
    try:
        with open('keys.json') as f:
            key = json.load(f)["news"]
    except:
        flash("Key error.")
        return redirect("/")
    try:
        req=urllib.request.urlopen(url_stub+key)
        fin=json.loads(req.read())
    except:
        flash("API Error")
        return redirect("/")
    return render_template("news.html",
                               news=fin["results"])

@app.route("/transit")
def transit():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    try:
        with open("keys.json") as f:
            traffic_key = json.load(f)["traffic"]
    except:
        flash("Key Error")
        return redirect("/")
    try:
        data = json.loads((urllib.request.urlopen("https://www.mapquestapi.com/traffic/v2/incidents?&outFormat=json&boundingBox=40.790419549617724%2C-73.8229751586914%2C40.635840993386466%2C-74.19136047363281&key="+ traffic_key)).read())
        incidents = []
        for x in range(0,5):
            incidents.append(data["incidents"][x]["shortDesc"])
    except:
        print("traffic")
        flash("API Error")
        return redirect("/")
    schoollat = getSchoolLocation(session["user"])[0]
    schoollong = getSchoolLocation(session["user"])[1]
    homelat = getUserLocation(session["user"])[0]
    homelong = getUserLocation(session["user"])[1]
    try:
        with open("keys.json") as f:
            app_id = json.load(f)["commuteID"]
        with open("keys.json") as s:
            app_code = json.load(s)["commuteCode"]
    except:
        flash("Key Error")
        return redirect("/")
    url = "https://transit.api.here.com/v3/route.json?app_id=" + app_id + "&app_code=" + app_code + "&routing=all&dep=" + str(homelat) + "," + str(homelong) + "&arr=" + str(schoollat) + "," + str(schoollong) + "&time=2018-11-27T07%3A30%3A00"
    print(url)
    #try:
    data = json.loads((urllib.request.urlopen(url)).read())
    stations = []
    for x in range(1, (len(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"]) - 1)):
        #print(str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Arr"]["Stn"]["name"]))
        if data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]['mode'] == 20:
            stations.append("Walk from "
                            + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Dep"]["Stn"]["name"])
                            + " to "
                            + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Arr"]["Stn"]["name"]))
        elif data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]['mode'] == 4 or 5 or 6 or 7:
            stations.append("The "
                + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Dep"]["Transport"]["name"])
                + " from "
                + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Dep"]["Stn"]["name"])
                + " to "
                + str(data["Res"]["Connections"]["Connection"][0]["Sections"]["Sec"][x]["Arr"]["Stn"]["name"]))
        else:
            print("api issues")
        #print("stations: " + str(stations))
        '''
    except:
        print("commute error")
        flash("API Error")
        return redirect("/")
        '''
    return render_template("traffic.html",
                           accidents=incidents,
                           route=stations)

@app.route("/weather")
def weather():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    url = "https://api.openweathermap.org/data/2.5/weather?zip=10282,us&units=imperial&appid="
    try:
        with open('keys.json') as f:
            key = json.load(f)["weather"]
    except:
        flash("Key Error")
        return redirect("/")
    url += key
    try:
        result = json.loads(urllib.request.urlopen(url).read())
    except:
        flash("API Error")
        return redirect("/")
    return render_template('weather.html', temp=result["main"]["temp"], desc=result["weather"][0]["description"].capitalize())

app.debug=True
app.run()
