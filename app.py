# Team Tails - Max Millar, Isaac Jon, Emily Lee, Brian Lee  

from flask import Flask, request, session, redirect, render_template, flash

app = Flask(__name__)

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
        # TODO: Validate user input and edit session
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        return redirect('/')

@app.route('/register')
def register():
    return render_template("register.html")

app.debug=True
app.run()
