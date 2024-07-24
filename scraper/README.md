# News Dashboard - Web Scraper

## Description

The Headline Scraper gathers headlines from various news source's front pages,
performs sentiment analysis on them, and then places them into a PostgreSQL database

The scraper expects the database to use the sources and headlines tables found
in the *database/schema.sql* file of this project. When scraping the front page of
a news source the scraper will first insert an entry for that news source (consisting
of a source name and a URL) into the sources table if it's not already present.
It will then insert each headline into the database, with headlines having the
following fields: text, date, sentiment, source

## Installation & Configuration

The following steps must be taken before the scraper can be used:

1. **Install python3:** Ensure that python3 has been installed
2. **Install Dependencies:** Install the project's dependencies, listed in the requirements.txt file of the scraper's folder:

    ```shell
    pip install -r requirements.txt
    ```

3. **Setup PostgreSQL Database:** Create a PostgreSQL database with the schema found in *database/schema.sql*. This database must be running when the scraper is run

4. **Configure Database Connection:** Create a file named database.ini in the same folder as the scraper. This file must have a section called postgresql_conn_data that contains all the information necessary to connect to your database. Here's an example of such a file:
  
    ```INI
    [postgresql_conn_data]
    host=localhost
    port=5432
    dbname=news
    ```

## Usage

The scraper can be run with either `python3 headline_scraper.py` or `./headline_scraper.py`

If you need to run it regularly as I need to in order to gather data for my News
Dashboard you can also schedule it using the cron command line utility