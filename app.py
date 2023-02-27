from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
DATABASE = "smilecafe.db"
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ueuywq9571"
db_name = "template/smilecafe.db"
def open_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except Error as e:
        print(e)
    return None

def is_logged_in():
    if session.get('email') is None:
        print("Not logged in")
        return False
    else:
        print("Logged in")
        return True


@app.route('/')
def render_home():  # put application's code here
    return render_template("home.html", logged_in=is_logged_in())


@app.route('/menu/<cat_id>')
def render_menu(cat_id):  # put application's code here
    con = open_database(DATABASE)
    query = "SELECT * FROM category"
    cur = con.cursor()
    cur.execute(query)
    category_list = cur.fetchall()
    print(category_list)
    query = "SELECT * FROM product WHERE cat_id = ? ORDER by name"
    cur = con.cursor()
    cur.execute(query, (cat_id, ))
    product_list = cur.fetchall()
    con.close()
    return render_template("menu.html", catergories=category_list, products=product_list, logged_in=is_logged_in())


@app.route('/contact')
def render_contact():  # put application's code here
    return render_template("contact.html", logged_in=is_logged_in())

@app.route('/login')
def render_login():
    if is_logged_in():
        return redirect('/')
    print("logging in")
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        print(email)
        query = """SELECT id, fname, password FROM user WHERE email = ?"""
        con = open_database(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()
        print(user_data)
        try:
            user_id = user_data[0]
            first_name = user_data[1]
            db_password = user_data[2]
        except IndexError:
            return("/login?error=Email+invalid+or+password+incorrect")

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['firstname'] = first_name

        print(session)
        return redirect('/')
    return render_template("login.html", logged_in=is_logged_in())
@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/?=See+You+Later!')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if is_logged_in():
        return redirect('/?message=Already+Logged+In')
    if request.method == 'POST':
        print(request.form)


if __name__ == '__main__':
    app.run()
