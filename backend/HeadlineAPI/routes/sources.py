from flask import request
from app import app
from models import Source
from db_service import fetch_data
from app import source_parser, lexer

@app.route('/sources', methods=['GET'])
def get_sources():
    filters = request.args.get("$filter")
    top = request.args.get("$top")
    skip = request.args.get("$skip")

    if filters:
        filters = source_parser.parse(filters, lexer=lexer)
    if top:
        top = int(top)
    if skip: 
        skip = int(skip)

    return fetch_data(Source, filters, top, skip)