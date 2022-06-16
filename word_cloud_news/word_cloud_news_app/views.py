from flask import render_template,  request
from word_cloud_news_app import app
from word_cloud_news_app import db as db_module

from datetime import date

from wordcloud import WordCloud, STOPWORDS
import base64
import io
from PIL import Image

@app.route("/", methods=('GET', 'POST'))
def hello_world():
    client = db_module.get_db()
    db = client.news_word_cloud
    headlines = db.daily_news_headlines


    headline_dates = headlines.find({}, {"date": 1}).sort("date")
    date_list = []
    for headline_date in headline_dates:
        date_list.append(headline_date["date"])

    # if method is 'POST', user may have specified date other than the current 
    # date and to only include specefic sources
    if request.method == 'POST':
        date_info = headlines.find_one({"date" : date_list[int(request.form['dateIndex'])]})
        sources = date_info['sources']

        included_source_list = request.form.getlist('sources_to_show')
        sources = [source for source in sources if source['source_name'] in included_source_list]
    else: 
        date_info = headlines.find_one({"date" : date.today().strftime("%y/%m/%d")})
        sources = date_info['sources']


    wordcloud = create_wordcloud(sources)
    image_array = wordcloud.to_array()
    img = Image.fromarray(image_array.astype('uint8'))

    # Stores image as bytes in in-memory buffer encoded using Base64
    file_object = io.BytesIO()
    img.save(file_object, 'png')
    encoded_img_data = base64.b64encode(file_object.getvalue())
    
    return render_template("index.html", 
                            user_image = encoded_img_data.decode('utf-8'), 
                            date_list = date_list)

def create_wordcloud(sources):
    word_list = ""
    for source in sources:
        headline_list = source['headlines']
        for headline in headline_list:
                word_list += headline

    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(width = 800, height = 600,
                        background_color ='black',
                        stopwords = stopwords,
                        min_font_size = 10).generate(word_list)
    return wordcloud

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500