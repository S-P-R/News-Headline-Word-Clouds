from app import app
from models import Headline
from db_service import fetch_headlines

@app.route('/headlines', methods=['GET'])
def get_headlines():
    return fetch_headlines()