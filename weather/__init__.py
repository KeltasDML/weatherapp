from flask import Flask,render_template,request,abort
from flask_sqlalchemy import SQLAlchemy
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '0d645e4092ffb279ac107ba3'
db = SQLAlchemy(app)

from weather import routes
