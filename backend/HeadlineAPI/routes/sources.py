from flask import request
from app import app
from models import Source
from db_service import fetch_sources
from app import source_parser, lexer

@app.route('/sources', methods=['GET'])
def get_sources():
    filters = request.args.get("$filter")
    if filters:
        filters = source_parser.parse(filters, lexer=lexer)

    return fetch_sources(filters)