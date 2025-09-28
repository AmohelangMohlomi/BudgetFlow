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

load_dotenv() 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/add-expense")
def add_expense():
    return render_template("add-expense.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/penny")
def penny():
    return render_template("penny.html")

@app.route("/budget")
def budget():
    return render_template("budget.html")

if __name__=="__main__":
    app.run(debug=True)