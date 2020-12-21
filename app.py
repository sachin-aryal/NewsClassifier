import pickle

from flask import Flask, render_template, jsonify
from lib import kathmandu_post, nb_predictor

app = Flask(__name__)
app.loaded_vectorizer = pickle.load(open('lib/vectorizer.pickle', 'rb'))
app.loaded_model = pickle.load(open('lib/classification.model', 'rb'))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route("/news")
def get_news():
    news = kathmandu_post.scrape()
    print(len(news))
    news_class = {
        1: [],
        0: [],
        -1: [],
    }
    for title in news:
        result = nb_predictor.predict(title)[0]
        news_class[result].append(title)
    return jsonify(news_class)


if __name__ == '__main__':
    app.run()
