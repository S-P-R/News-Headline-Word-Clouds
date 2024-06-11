from flask import request
from app import app
from models import Headline
from db_service import fetch_data
from app import headline_parser, lexer

@app.route('/headlines', methods=['GET'])
def get_headlines():
    filters = request.args.get("$filter")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    if filters:
        filters = headline_parser.parse(filters, lexer=lexer) 
    if top:
        top = int(top)
    if skip: 
        skip = int(skip)
   
    return fetch_data(Headline, filters, top, skip)
