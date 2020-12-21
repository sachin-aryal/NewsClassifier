import csv
import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics


# Read in the training data.
with open("sentiment_data.csv", 'r') as file:
    data = list(csv.reader(file))

final_data = [row for row in data if len(row) == 2]

vectorizer = CountVectorizer(stop_words='english')
# Total Count: 162973
train_data = final_data[150000:]
test_data = final_data[150000:]
train_features = vectorizer.fit_transform([r[0] for r in train_data])
test_features = vectorizer.transform([r[0] for r in test_data])

# Fit a naive bayes model to the training data.
# This will train the model using the word counts we computer, and the existing classifications in the training set.
nb = MultinomialNB()
nb.fit(train_features, [int(r[1]) for r in train_data])

pickle.dump(vectorizer, open('vectorizer.pickle', 'wb'))
pickle.dump(nb, open('classification.model', 'wb'))

# Now we can use the model to predict classifications for our test features.
predictions = nb.predict(test_features)
actual = [int(r[1]) for r in test_data]
# Compute the error.  It is slightly different from our model because the internals of this process work
# differently from our implementation.
fpr, tpr, thresholds = metrics.roc_curve(actual, predictions, pos_label=1)
print("Multinomial naive bayes AUC: {0}".format(metrics.auc(fpr, tpr)))

# Result: Multinomial naive bayes AUC: 0.8741172716402508