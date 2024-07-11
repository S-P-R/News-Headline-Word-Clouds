"""
File: headlines.py
Author: Sean Reilly
Description: Contains HTTP routes to interact with news headlines
"""

from flask import request, jsonify
from app import app
from models import Headline
from db_service import fetch_data
from app import headline_parser, lexer
from exceptions import FilterParseException, OrderByException
from sqlalchemy.exc import SQLAlchemyError
from utils import process_orderby

@app.route('/headlines', methods=['GET'])
def get_headlines():
    filters = request.args.get("$filter")
    ordering = request.args.get("$orderby")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    try: 
        if filters:
            filters = headline_parser.parse(filters, lexer=lexer) 
        if ordering:
           ordering = process_orderby(Headline, ordering)
        if top:
            top = int(top)
        if skip: 
            skip = int(skip)
        
        return fetch_data(Headline, filters, ordering, top, skip)
    except (FilterParseException, OrderByException) as e:
        return jsonify(error=e.message), 400
    except ValueError: 
        return jsonify(error="$top and $skip must be integers"), 400
    except SQLAlchemyError:
        return jsonify(error="There was an error retrieving data from the database"), 500
    except Exception:
        return jsonify(error="An unexpected error occured"), 500
