CREATE SCHEMA news_headlines;

create table news_headlines.source (
    name VARCHAR(50) PRIMARY KEY, 
    link VARCHAR(50)
);

create table news_headlines.headline (
    text VARCHAR (100) NOT NULL,
    date DATE NOT NULL, 
    sentiment DECIMAL CHECK (sentiment >= -1 AND sentiment <= 1), 
    source VARCHAR(50) references news_headlines.source(name),
    PRIMARY KEY (text, date)
);

CREATE INDEX headline_date_idx ON news_headlines.headline (date);
CREATE INDEX headline_date_source_idx ON news_headlines.headline (date, source);