from flask import Flask, render_template
import sqlite3
from sqlite3 import Error
DATABASE = "smilecafe.db"
app = Flask(__name__)

def open_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_home():  # put application's code here
    return render_template("home.html")


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
    return render_template("menu.html", catergories=category_list, products=product_list)


@app.route('/contact')
def render_contact():  # put application's code here
    return render_template("contact.html")


if __name__ == '__main__':
    app.run()
