from app import app
from flask import Blueprint
from db_service import fetch_dates

@app.route('/dates', methods=['GET'])
def get_dates():
    return fetch_dates()