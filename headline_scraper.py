#!/usr/bin/env python3
"""
File: headline_scraper.py
Author: Sean Reilly
Description: Scrapes news headlines and adds them to a Postgres database
"""

import requests
from bs4 import BeautifulSoup
from datetime import date
import psycopg2
import psycopg2.extras
import logging
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import configparser

MAX_HEADLINE_LENGTH = 100
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s")
sid_obj= SentimentIntensityAnalyzer()

def connect_to_db() -> psycopg2.extensions.connection:
    """Returns a connection to a Postgres database"""
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read("database.ini")
        config_params = config_parser.items("postgresql_conn_data")
        db_conn_dict = {}
        for name, value in config_params:
            db_conn_dict[name] = value
        return psycopg2.connect(**db_conn_dict)
    except (configparser.Error, psycopg2.Error) as e:
        logging.critical(e)
        raise ConnectionError("Failed to connect to Postgres database")

def calculate_sentiment(s : str) -> float:
    """Returns the sentiment (between -1 and 1) of a string"""
    sentiment_dict = sid_obj.polarity_scores(s)
    return sentiment_dict["compound"]

conn = connect_to_db()
cursor = conn.cursor()

# Array of news source homepages to crawl for headlines. Each source has a
# name, a link, and an attribute, attribute-value pair that identify headlines
to_crawl = [("New York Times", "https://www.nytimes.com/", {"class": re.compile("indicate-hover")}),
            ("Washington Post", "https://www.washingtonpost.com/", {"data-pb-local-content-field": "web_headline"}),
            ("Fox News", "https://www.foxnews.com/", {"class": "title"}), 
            ("BBC", "https://www.bbc.com/", {"data-testid": re.compile("headline")}),  
            ("Al Jazeera", "https://www.aljazeera.com/", {"class": "u-clickable-card__link"}), 
            ("South China Morning Post", "https://www.scmp.com/", {"data-qa": "ContentHeadline-Headline"})]
       
for source_name, URL, filters in to_crawl:
    try:
        # Enter source into db if it doesn"t already exist
        cursor.execute("INSERT INTO news_headlines.source VALUES (%s, %s) ON CONFLICT DO NOTHING", (source_name, URL))
        conn.commit()

        page = requests.get(URL, headers={"user-agent": "wc-headline-scraper"})
        soup = BeautifulSoup(page.content, "html.parser")
        elements = soup.find_all(attrs=filters)

        headlines = [element.get_text(strip=True) for element in elements]
        headlines = [headline.replace("\xad", "") for headline in headlines] # Remove soft hyphens
        headlines = list(set(headlines)) # Filter out duplicates 
        # Unlikely to be actual headline if under 4 words
        headlines = filter(lambda h: len(h.split()) > 3 and len(h) <= MAX_HEADLINE_LENGTH, headlines) 
        headline_data = [(headline, date.today(), calculate_sentiment(headline), source_name) for headline in headlines]

        query = "INSERT INTO news_headlines.headline(text, date, sentiment, source) VALUES (%s, %s, %s, %s)"
        psycopg2.extras.execute_batch(cursor, query, headline_data)
        conn.commit()
        logging.info(f"Finished {source_name}")
    except (psycopg2.Error, requests.exceptions.RequestException) as e:
        conn.rollback()
        logging.error(f"{source_name} Failed: {e}")

conn.close()