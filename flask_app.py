from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle

import os
import numpy as np

# import HashingVectorizer from local dir
from vectorizer import vect

app = Flask(__name__)

######## Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))

def classify(document):
    label = {-1:'Stressed', 0:'Neutral', 1:'Without stress'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba


######## Flask
class TweetForm(Form):
    tweet = TextAreaField('',
                         [validators.DataRequired(),
                         validators.length(min=15)])

@app.route('/')
def index():
    form = TweetForm(request.form)
    return render_template('tweetform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = TweetForm(request.form)
    if request.method == 'POST' and form.validate():
        tweet = request.form['tweet']
        y, proba = classify(tweet)
        return render_template('results.html',
                                content=tweet,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('tweetform.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)