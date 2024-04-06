from app import app
from models import Source
from db_service import fetch_sources

@app.route('/sources', methods=['GET'])
def get_sources():
    return fetch_sources()