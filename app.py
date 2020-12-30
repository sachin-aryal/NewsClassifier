import pickle

from flask import Flask, render_template
from lib import kathmandu_post, nb_predictor

app = Flask(__name__)
app.loaded_vectorizer = pickle.load(open('lib/vectorizer.pickle', 'rb'))
app.loaded_model = pickle.load(open('lib/classification.model', 'rb'))


@app.route('/')
def index():
    news = kathmandu_post.scrape()
    news_content = {}
    for title, content in news.items():
        sentiment_class = nb_predictor.predict(title)[0]
        news_content[title] = [content, sentiment_class]
    return render_template('index.html', **{"news_content": news_content})


if __name__ == '__main__':
    app.run(debug=True)
