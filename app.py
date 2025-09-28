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


if __name__=="__main__":
    app.run(debug=True)