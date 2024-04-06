from models import Headline
from models import Source

def fetch_headlines():
  return Headline.query.all()

def fetch_sources():
    return Source.query.all()

def fetch_dates():
   return [{"placeholder-value": 0}]

