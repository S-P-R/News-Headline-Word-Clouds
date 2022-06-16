from flask import g
from pymongo import MongoClient
from flask import current_app
from word_cloud_news_app import app



def get_db():
    if 'db' not in g:
        g.db = connect_to_database()

    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def connect_to_database():
    CONNECTION_STRING = "mongodb+srv://SPR:upQEVi7ckhI05C82@cluster0.nbkwl.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client