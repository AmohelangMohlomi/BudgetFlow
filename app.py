from flask import Flask, render_template, request, redirect, url_for, flash, g, session, jsonify
from dotenv import load_dotenv
import os
import sqlite3
import random
import requests
import markdown
import matplotlib
import matplotlib.pyplot as plt   
import numpy as np
from functools import wraps

load_dotenv() 

app = Flask(__name__)
DATABASE = 'users.db'
app.secret_key = 'your_secret_key' 

@app.route("/")
def index():
    return render_template("index.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)
        if user and user['password'] == password:  
            session['username'] = username  
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'error')

    return render_template("login.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('signup.html')

        success = add_user(username, password)  

        if success:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')

    return render_template('signup.html')

@app.route("/add-expense", methods=["GET", "POST"])
@login_required
def add_expense():
    if 'username' not in session:
        flash("Please login to add expenses.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        date = request.form.get("date")

        user = get_user(session["username"])
        user_id = user["id"]

        save_expense(user_id, amount, category, description, date)
        flash("Expense added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add-expense.html")


@app.route("/dashboard")
@login_required
def dashboard():
    if 'username' not in session:
        flash("Please login to access the dashboard.", "error")
        return redirect(url_for("login"))

    user = get_user(session['username'])
    user_id = user["id"]
    expenses = get_user_expenses(user_id)

    return render_template("dashboard.html", expenses=expenses)


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/penny")
@login_required
def penny():
    return render_template("penny.html")

@app.route("/budget")
@login_required
def budget():
    return render_template("budget.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# Connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close DB when app context ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        db.commit()



def get_user(username):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone()

def add_user(username, password):
    try:
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    
def save_expense(user_id, amount, category, description, date):
    db = get_db()
    db.execute(
        '''
        INSERT INTO expenses (user_id, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (user_id, amount, category, description, date)
    )
    db.commit()

def get_user_expenses(user_id):
    db = get_db()
    cursor = db.execute(
        '''
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
        ''',
        (user_id,)
    )
    return cursor.fetchall()


if __name__=="__main__":
    init_db()
    app.run(debug=True)