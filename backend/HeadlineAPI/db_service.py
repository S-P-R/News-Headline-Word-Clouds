"""
File: db_service.py
Author: Sean Reilly
Description: Handles interactions with the application's database
"""

from app import db

def fetch_data(to_fetch, filters = None, limit : int = None, offset : int = None):
    """
    Fetches data from a SQLAlchemy database session

    Args:
        to_fetch: An object that maps onto the database data that's should be fetched
        filters: Filters used to filter the data being fetched
        limit: A Maxiumum # of db rows to retrieve 
        offset: A number of rows to be skipped/not-fetched

    Returns:
        A list of values taken from the database
    """

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

