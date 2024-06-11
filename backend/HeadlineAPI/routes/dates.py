from app import app
from flask import request
from db_service import fetch_data
from models import DateSummary
from app import date_parser, lexer

@app.route('/dates', methods=['GET'])
def get_dates():
    filters = request.args.get("$filter")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    if filters:
        filters = date_parser.parse(filters, lexer=lexer)
    if top:
        top = int(top)
    if skip: 
        skip = int(skip)

    return fetch_data(DateSummary, filters, top, skip)