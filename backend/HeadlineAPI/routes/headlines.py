from flask import request, jsonify
from app import app
from models import Headline
from db_service import fetch_data
from app import headline_parser, lexer
from exceptions import FilterParseException
from sqlalchemy.exc import SQLAlchemyError

@app.route('/headlines', methods=['GET'])
def get_headlines():
    filters = request.args.get("$filter")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    try: 
        if filters:
            filters = headline_parser.parse(filters, lexer=lexer) 
        if top:
            top = int(top)
        if skip: 
            skip = int(skip)
        
        return fetch_data(Headline, filters, top, skip)
    except ValueError: 
        return jsonify(error="$top and $skip must be integers"), 400
    except FilterParseException:
        return jsonify(error="$filter syntax could not be successfully parsed"), 400
    except AttributeError:
        return jsonify(error="properties in $filter must be either text, date, sentiment or source"), 400
    except SQLAlchemyError:
        return jsonify(error="There was an error retrieving data from the database"), 500
    except Exception:
        return jsonify(error="An unexpected error occured"), 500
