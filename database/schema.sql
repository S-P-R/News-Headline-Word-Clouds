CREATE SCHEMA news_headlines;

create table news_headlines.news_source (
    name VARCHAR(20) PRIMARY KEY, 
    link VARCHAR(50)
);

create table news_headlines.headline (
    text VARCHAR (100) NOT NULL,
    stripped_text VARCHAR (100),
    date DATE NOT NULL, 
    sentiment DECIMAL CHECK (sentiment >= 0 AND sentiment <= 1), 
    source VARCHAR(20) references news_headlines.news_source(name),
    PRIMARY KEY (text, date)
);

CREATE INDEX headline_date_idx ON news_headlines.headline (date);
CREATE INDEX headline_date_source_idx ON news_headlines.headline (date, source);