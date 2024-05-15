from flask import request
import re # TODO: remove?
from app import app
from models import Headline
from db_service import fetch_headlines
from app import headline_parser, lexer

@app.route('/headlines', methods=['GET'])
def get_headlines():
    filters = request.args.get("$filter")

    top = request.args.get("top")

    if filters:
        print("IN fileters")
        filters = headline_parser.parse(filters, lexer=lexer)
        
    if top:
        print("Top: ", top)

    return fetch_headlines(filters)
