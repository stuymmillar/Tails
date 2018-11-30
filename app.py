# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee  

import os
import json
import urllib

from flask import Flask, request, session, redirect, render_template, flash

from util.manage_user import register_user, validate_login

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/')
def home():
    if "loggedin" not in session:
        return redirect('/login')
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        success, message = validate_login(username, password)
        print(message)
        flash(message)
        if success:
            session["loggedin"] = True
            return redirect('/')
        else:
            return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # TODO: finish this
        return "temp :3"

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
