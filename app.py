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
    url_stub="http://api.nytimes.com/svc/topstories/v2/home.json?api-key="
    key="ed4eb13cfbb047da88ca5ab676989676"
    req=urllib.request.urlopen(url_stub+key)
    fin=json.loads(req.read())

    return render_template("news.html",
                               news=fin["results"])

app.debug=True
app.run()
