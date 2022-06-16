import requests
from bs4 import BeautifulSoup
from datetime import date

from pymongo import MongoClient
import dns

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Array of news sources to crawl for headlines. Each source has a name, a link,
# the tag html tag used to represent most headlines and the name of the class
# associated with those headlines
to_crawl = [("BBC", "https://www.bbc.com/", "a", "media__link"),
            ("Fox News", "https://www.foxnews.com/", "h2", "title"),
            ("Al Jazeera", "https://www.aljazeera.com/", "a", "u-clickable-card__link"),
            ("New York Times", "https://www.nytimes.com/", "div", "css-xdandi"),
            ("Vox", "https://www.vox.com/", "h2", "c-entry-box--compact__title"),
            ("The Guardian", "https://www.theguardian.com/world", "a", "u-faux-block-link__overlay js-headline-text")]

# dict with dates as key, containing dicts with newssource as key, containing 
# a list of article titles
daily_news_dict = {
    "date": date.today().strftime("%y/%m/%d"),
    "sources": []
    }

for news_source in to_crawl:
    URL = news_source[1]
    source_dict = {
        "source_name": news_source[0],
        "source_link": URL, 
        "headlines": []
    }
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Note: the find_all method is used rather than the seemingly more simple 
    #       select method because the select method doesn't work for class names
    #       containing whitespace
    elements = soup.find_all(news_source[2], class_=news_source[3])
    for element in elements:
            source_dict["headlines"].append(element.text.strip())
    
    daily_news_dict["sources"].append(source_dict)
    print("Finished " + URL)


CONNECTION_STRING = "mongodb+srv://SPR:upQEVi7ckhI05C82@cluster0.nbkwl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

db = client.news_word_cloud
headlines = db.daily_news_headlines
headlines.insert_one(daily_news_dict)