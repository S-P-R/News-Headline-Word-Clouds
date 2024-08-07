"""
File: models.py
Author: Sean Reilly
Description: Defines models that correspond to data representations within the
             application's database
"""

from dataclasses import dataclass
from datetime import date as datetype
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

@dataclass
class Source(db.Model):
    __tablename__ = 'source'
    __table_args__ = {'schema': 'news_headlines'}
    # model type annotations are used by filter_parser for type checking
    name: str
    link: str

    name = db.Column(db.String(50), primary_key=True)
    link = db.Column(db.String(50))
    headlines = db.relationship('Headline')

@dataclass
class Headline(db.Model):
    __tablename__ = 'headline'
    __table_args__ = {'schema': 'news_headlines'}
    text: str
    sentiment: float
    source: str

    text = db.Column(db.String(100), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    sentiment = db.Column(db.Float)
    source = db.Column(db.String(50), db.ForeignKey('news_headlines.source.name'), nullable=False)

@dataclass
class DateSummary(db.Model):
    __tablename__ = 'date_summary'
    __table_args__ = {'schema': 'news_headlines'}
    date: datetype
    avg_sentiment: float
    
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.Float)
   
    