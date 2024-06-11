from flask import jsonify
from app import db
from models import Headline, Source, DateSummary

def fetch_data(to_fetch, filters = None, limit : int = None, offset : int = None):
    query = db.select(to_fetch)
    if filters is not None:
         query = query.filter(filters)
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    
    result = db.session.execute(query).scalars()
    serialized_result = serialize(result)
    return serialized_result

def serialize (to_serialize):
    return [{column.name: getattr(row, column.name) for column in row.__table__.columns} for row in to_serialize]

