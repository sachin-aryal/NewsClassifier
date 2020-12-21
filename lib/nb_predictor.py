from flask import current_app


def predict(text):
    check = current_app.loaded_vectorizer.transform([text])
    return current_app.loaded_model.predict(check)
