from __future__ import print_function
import csv
import math
import os
import sys
import time
import requests
import json
import psycopg2
import argparse
import lxml.html
import io
import nltk
import emoji
from datetime import date
from flask_mail import Mail, Message
from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint,jsonify
from tempfile import mkdtemp
from flask_session import Session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from lxml.cssselect import CSSSelector
from flask import (Blueprint, Flask, flash, g, redirect, render_template,
                   request, send_file, session, url_for)
from bs4 import BeautifulSoup

from textblob import TextBlob
from googletrans import Translator

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True, static_url_path="", static_folder="static")
app.config.from_pyfile('config.cfg')

app.config['SESSION_FILE_DIR'] = mkdtemp()
Session(app)
con = psycopg2.connect(dbname=app.config['DBNAME'],user=app.config['DBUSER'],host=app.config['HOST'],password=app.config['PASSWORD'])

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=app.config['DBUSER'],pw=app.config['PASSWORD'],url=app.config['URL'],db=app.config['DBNAME'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def deEmojify(inputString):
    return emoji.get_emoji_regexp().sub(u'', inputString)
    # return inputString.encode('ascii', 'ignore').decode('ascii')

# returns sentiment for english statements
def getSentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

# returns sentiment for mixed languages sentiments
def getMixedSentiment(text):
    translator = Translator()
    text=deEmojify(text)
    text=translator.translate(text).text
    return getSentiment(text)

def execute_db(query,args=()):
    cur = con.cursor()
    cur.execute(query,args)
    con.commit()
    cur.close()
def query_db(query,args=(),one=False):
    cur = con.cursor()
    result=cur.execute(query,args)
    values=cur.fetchall()
    return values

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("adminid") is None:
#             return redirect(url_for("auth.login"))
#         return f(*args, **kwargs)
#     return decorated_function

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("admin")==False:
#             return redirect(url_for("main.index", next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function
    
# Importing Blueprints
from app.views.main import main
from app.views.scraping.flipkart import flipkart
from app.views.scraping.youtube import youtube
# Registering Blueprints
app.register_blueprint(main)
app.register_blueprint(flipkart)
app.register_blueprint(youtube)
