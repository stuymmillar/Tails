# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee  

import os

from flask import Flask, request, session, redirect, render_template, flash

from util.manage_user import register_user, validate_login

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/')
def home():
    if "loggedin" not in session:
        flash("You must be logged in to access Tailos.", 'alert')
        return redirect('/login')
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return redirect('/')
        else:
            return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']
        print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        if not (username and password and re_password
                and school_id and longitude and latitude):
            flash("One or more fields missing.", 'alert')
            return render_template("register.html")
        if password != re_password:
            flash("Passwords do not match.", 'alert')
            return render_template("register.html")
        success = register_user(username, password, password,
                                school_id, longitude, latitude)
        if success:
            flash("Registered {}".format(username), 'success')
            return redirect('login')
        else:
            flash("Username {} already exists.".format(username), 'alert')
            return redirect('register')

app.debug=True
app.run()
