"""
File: app.py
Author: Sean Reilly
Description: Root file of the API
"""
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_CONN_STRING")
CORS(app)
db.init_app(app)

from filter_parser import construct_parser
from models import Headline, Source, DateSummary

headline_parser, lexer  = construct_parser(Headline)
source_parser, _  = construct_parser(Source)
date_parser, _  = construct_parser(DateSummary)

from routes import headlines
from routes import sources
from routes import dates