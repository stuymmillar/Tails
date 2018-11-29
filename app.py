# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee  

import os

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
        # Display login form
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
    success, message = register_user('test', 'Bop', 'Brooklyn Tech', 3, 3)
    print(message)
    success, message = register_user('iidxgold', 'money', 'Brooklyn Tech', 3, 3)
    print(message)
    return render_template("register.html")

app.debug=True
app.run()
