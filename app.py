from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load model and vectorizer
model = None
vectorizer = None

try:
    if os.path.exists('model.pkl'):
        model = pickle.load(open('model.pkl', 'rb'))
    if os.path.exists('vectorizer.pkl'):
        vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
except Exception as e:
    print(f"Error loading pkl: {e}")

# If pkl not fitted or not exists, create dummy fitted vectorizer to avoid crash
from sklearn.feature_extraction.text import TfidfVectorizer
if vectorizer is None:
    print("Creating fallback fitted vectorizer...")
    # Dummy fit to prevent NotFittedError
    vectorizer = TfidfVectorizer()
    vectorizer.fit(["This is real news", "This is fake news sample text"])

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        news = request.form.get('news', '')
        if news and model and vectorizer:
            try:
                vec = vectorizer.transform([news])
                pred = model.predict(vec)[0]
                # 0 = Real, 1 = Fake (adjust based on your training)
                result = "FAKE NEWS" if pred == 1 else "REAL NEWS"
            except Exception as e:
                result = f"Error during prediction: {str(e)}"
        elif not model:
            result = "Model not loaded! Check model.pkl in repo."
        else:
            result = "Please enter some news text"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



 
