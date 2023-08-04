from flask import flash, render_template, Flask, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

from sqlhelpers import *
from forms import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '18042001Khoi'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET'] = 'secret123'

mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, please login!", 'danger')
            return redirect(url_for('login'))
    return wrap
def login_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username",username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")

    if 'POST' == request.method and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if isnewuser(username): #check new user
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            login_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash("User already exit!", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        candidate = request.form['password']

        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username",username)
        accpass = user.get('password')

        if accpass is None:
            flash("Username not found!", 'danger')
            return redirect(url_for('login'))
        elif sha256_crypt.verify(candidate,accpass):
            login_user(username)
            flash("Login success!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalided password!", 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", 'success')
    return redirect(url_for('login'))
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template('dashboard.html', session=session)
@app.route("/")
def index():
    test()
    # users = Table("users","name","email","username","password")
    # users.insert("John","john@gmail.com","johnJ","hash")
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)