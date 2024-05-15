from dataclasses import dataclass
from datetime import date as datetype
from app import db

@dataclass
class Source(db.Model):
    __tablename__ = 'source'
    __table_args__ = {'schema': 'news_headlines'}
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
    date: datetype
    sentiment: float
    source: str

    text = db.Column(db.String(100), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    sentiment = db.Column(db.Float)
    source = db.Column(db.String(50), db.ForeignKey('news_headlines.source.name'), nullable=False)
    