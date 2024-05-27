from app import app
from flask import request
from db_service import fetch_dates
from app import date_parser, lexer

@app.route('/dates', methods=['GET'])
def get_dates():
    filters = request.args.get("$filter")
    if filters:
        filters = date_parser.parse(filters, lexer=lexer)
    return fetch_dates(filters)