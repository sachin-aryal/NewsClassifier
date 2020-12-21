import requests
import time
import random
import json
import os

from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://kathmandupost.com"
BASE_PATH = "lib"


def scrape():
    input_file = os.path.join(BASE_PATH, datetime.today().strftime('%Y-%m-%d')+"_news.json")
    if os.path.exists(input_file):
        with open(input_file) as fh:
            return json.load(fh)

    content = requests.get(BASE_URL).content
    bs = BeautifulSoup(markup=content, features='lxml')
    articles = bs.find_all("article", {"class": "article-image"})
    news_list = {}
    for article in articles:
        news_link = article.find("a", href=True)
        if news_link:
            news_list[news_link['href']] = news_link.getText()
    news_content_list = {}
    for each_news in news_list:
        content = requests.get(BASE_URL+each_news).content
        soup = BeautifulSoup(markup=content, features='lxml')
        title = soup.select('#mainContent > main > div > div:nth-child(2) > div.col-sm-8 > h1')
        if title:
            news_content = soup.find("section", {"class": "story-section"})
            if news_content and news_content.text:
                news_content_list[title[0].text] = news_content.text
        time.sleep(random.randint(1, 5))
    with open(input_file, "w") as fh:
        json.dump(news_content_list, fh, indent=4)
    return news_content_list