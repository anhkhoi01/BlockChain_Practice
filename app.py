from flask import flash, render_template, Flask, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

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

def login_user(username):
    pass
@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")

    if form.validate():
        print("form ok")

    if 'POST' == request.method:
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if isnewuser(username): #check new user
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            login_user(username)
            return redirect(url_for('dashboard'))
            # return render_template('dashboard.html')
        else:
            flash("User already exit!", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')
@app.route("/")
def index():
    # users = Table("users","name","email","username","password")
    # users.insert("John","john@gmail.com","johnJ","hash")
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)