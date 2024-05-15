from flask import jsonify
from app import db
from models import Headline
from models import Source

def fetch_headlines(filters):
    query = db.select(Headline)
    if filters is not None:
         query = query.filter(filters)
    
    result = db.session.execute(query).scalars()
    serialized_result = serialize(result)
    return serialized_result

def fetch_sources(filters):
    query = db.select(Source)
    if filters is not None:
         query = query.filter(filters)
    
    result = db.session.execute(query).scalars()
    serialized_result = serialize(result)
    return serialized_result

def fetch_dates():
   return [{"placeholder-value": 0}]

def serialize (to_serialize):
    return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in to_serialize]

