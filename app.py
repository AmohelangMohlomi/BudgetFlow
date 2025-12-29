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
    user = get_user(session['username'])
    user_id = user['id']

    budgets = get_user_budgets(user_id)   
    spending = get_spent_by_category(user_id)  

    spent_dict = {row['category']: row['spent'] for row in spending}

    categories = []
    budgets_list = []
    spent_list = []
    over_budget_alerts = []

    for b in budgets:
        cat = b['category']
        budget_amount = b['amount']
        spent_amount = spent_dict.get(cat, 0)

        categories.append(cat)
        budgets_list.append(budget_amount)
        spent_list.append(spent_amount)

        if spent_amount > budget_amount:
            over_budget_alerts.append({
                'category': cat,
                'budgeted': budget_amount,
                'spent': spent_amount,
                'difference': spent_amount - budget_amount
            })

    return render_template(
        "dashboard.html",
        categories=categories,
        budgets=budgets_list,
        spent=spent_list,
        expenses=get_user_expenses(user_id),
        over_budget_alerts=over_budget_alerts  
    )

@app.route("/get_penny_dashboard_advice", methods=["POST"])
@login_required
def get_penny_dashboard_advice():
    user = get_user(session['username'])
    user_id = user['id']

    budgets = get_user_budgets(user_id)
    spending = get_spent_by_category(user_id)

    summary_lines = []
    for b in budgets:
        category = b['category']
        budget = b['amount']
        spent = next((s['spent'] for s in spending if s['category'] == category), 0)
        diff = spent - budget

        summary_lines.append(f"{category}: Budgeted R{budget:.2f}, Spent R{spent:.2f} ({'Over' if diff > 0 else 'Under'} by R{abs(diff):.2f})")

    summary_text = "\n".join(summary_lines)
    prompt = (
        "You are Penny, a friendly budgeting assistant. "
        "Based on the following financial summary, give one short, specific, encouraging advice (max 2 sentences):\n"
        f"{summary_text}"
    )

    api_url = "https://api.shecodes.io/ai/v1/generate"
    api_key = os.getenv("SHECODES_API_KEY")

    try:
        response = requests.get(api_url, params={
            'prompt': prompt,
            'key': api_key
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            penny_advice = data.get("answer", "Couldn't generate advice right now.")
            penny_advice_structured= markdown.Markdown(penny_advice)
        else:
            penny_advice = "Error fetching Penny's advice."

    except Exception as e:
        penny_advice = f"Penny had trouble thinking: {str(e)}"

    return jsonify({'advice': penny_advice_structured})



@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


@app.route("/get_penny_response", methods=["POST"])
@login_required
def get_penny_response():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Missing user message'}), 400

    prompt = (
        "You are Penny, a helpful and friendly financial assistant. "
        "Provide practical budgeting, saving, or spending advice in response to the user's message: "
        f"'{user_message}'"
    )

    api_url = "https://api.shecodes.io/ai/v1/generate"
    api_key = os.getenv("SHECODES_API_KEY")

    try:
        response = requests.get(api_url, params={
            'prompt': prompt,
            'key': api_key
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            penny_reply = data.get("answer", "Sorry, I couldn't come up with advice right now.")
        else:
            penny_reply = "Error getting advice from Penny. Please try again later."

    except Exception as e:
        penny_reply = f"An error occurred: {str(e)}"

    session['penny_last'] = {
        'user_message': user_message,
        'penny_reply': penny_reply
    }

    return jsonify({'reply': penny_reply})

@app.route("/penny",methods=["GET","POST"])
@login_required
def penny():
    return render_template("penny.html")

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    if 'username' not in session:
        flash("Please login to access your budget.", "error")
        return redirect(url_for("login"))

    user = get_user(session['username'])

    if request.method == "POST":
        category = request.form.get("category")
        amount = float(request.form.get("amount"))

        success = save_budget(user['id'], category, amount)
        if success:
            flash(f"Budget for {category} set to ${amount:.2f}", "success")
        else:
            flash("Error saving budget. Try again.", "error")

    cursor = get_db().execute(
        "SELECT category, amount FROM budgets WHERE user_id = ?", (user['id'],)
    )
    budgets = cursor.fetchall()

    return render_template("budget.html", budgets=budgets)



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

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE(user_id, category),
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

def get_user_budgets(user_id):
    db = get_db()
    cursor = db.execute('''
        SELECT category, amount FROM budgets
        WHERE user_id = ?
    ''', (user_id,))
    return cursor.fetchall()

def get_spent_by_category(user_id):
    db = get_db()
    cursor = db.execute('''
        SELECT category, SUM(amount) as spent
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    ''', (user_id,))
    return cursor.fetchall()

def save_budget(user_id, category, amount):
    """Insert or update a budget entry for a user."""
    db = get_db()
    try:
        db.execute('''
            INSERT INTO budgets (user_id, category, amount)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, category) DO UPDATE SET amount = excluded.amount
        ''', (user_id, category, amount))
        db.commit()
        return True
    except Exception as e:
        print("Error saving budget:", e)
        return False



if __name__=="__main__":
    init_db()
    app.run(debug=True)