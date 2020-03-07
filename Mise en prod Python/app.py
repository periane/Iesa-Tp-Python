from flask import Flask, jsonify, request, render_template, redirect
import json
from wtforms import Form
from flask_cors import CORS
from joblib import load
		
app = Flask(__name__)

tweet=""
clf=load('filename.joblib')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        tweet = request.form['tweet']
        return redirect(request.url+'results')
    return render_template('index.html')

def return_probas():
  probas = clf.predict_proba([tweet.lower()]) 
  print(tweet)
  print(probas)
  probas_dict = {
                'hate speech':probas[0][0],
                'offensive language':probas[0][1],
                'neither':probas[0][2]
                }
  return jsonify(probas_dict)


@app.route('/result')
def results():
    return render_template('results.html', tweet=tweet, probas=return_probas())
		
if __name__ == '__main__':
    app.run(debug=True)