"""
File: dates.py
Author: Sean Reilly
Description: Contains HTTP routes to interact with the dates that headlines have
             been gathered for 
"""

from app import app
from flask import request, jsonify
from db_service import fetch_data
from models import DateSummary
from app import date_parser, lexer
from exceptions import FilterParseException
from sqlalchemy.exc import SQLAlchemyError

@app.route('/dates', methods=['GET'])
def get_dates():
    filters = request.args.get("$filter")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    try: 
        if filters:
            filters = date_parser.parse(filters, lexer=lexer)
        if top:
            top = int(top)
        if skip: 
            skip = int(skip)

        return fetch_data(DateSummary, filters, top, skip)
    except ValueError: 
        return jsonify(error="$top and $skip must be integers"), 400
    except FilterParseException as e:
        return jsonify(error=e.message), 400
    except SQLAlchemyError:
        return jsonify(error="There was an error retrieving data from the database"), 500
    except Exception:
        return jsonify(error="An unexpected error occured"), 500

