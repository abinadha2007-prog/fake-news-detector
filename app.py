from flask import Flask, render_template, request
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

# --- DATASET LOAD ---
def load_data():
    try:
        fake_df = pd.read_csv('Fake.csv')
        true_df = pd.read_csv('True.csv')
        fake_df['label'] = 0
        true_df['label'] = 1
        df = pd.concat([fake_df, true_df], ignore_index=True)
        df = df.sample(frac=1).reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

print("Loading data...")
df = load_data()

# --- MODEL TRAIN ---
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
model = LogisticRegression()

if df is not None:
    X = vectorizer.fit_transform(df['text'].astype(str))
    y = df['label']
    model.fit(X, y)
    print(f"Model Trained! Accuracy check done")
else:
    print("Dataset not found!")

# --- TRANSLATION ---
def translate_to_english(text):
    try:
        # Tamil irukka nu check pannu
        if any("\u0B80" <= char <= "\u0BFF" for char in text):
            translated = GoogleTranslator(source='ta', target='en').translate(text)
            return translated, text
        else:
            return text, None
    except Exception as e:
        print(f"Translation error: {e}")
        return text, None

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'), '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    original_text = ""
    translated_text = ""
    confidence = 0
    
    if request.method == 'POST':
        original_text = request.form['news']
        translated, was_tamil = translate_to_english(original_text)
        
        # Model ku English than
        text_for_model = clean_text(translated)
        vec = vectorizer.transform([text_for_model])
        
        # Confidence kooda vaanguren
        prob = model.predict_proba(vec)[0]
        pred = model.predict(vec)[0]
        
        translated_text = translated
        if was_tamil:
            translated_display = f"Translated: {translated}"
        else:
            translated_display = ""
            
        if pred == 1:
            confidence = prob[1] * 100
            result = f"TRUE NEWS ✅ ({confidence:.0f}% Confident)"
            result_type = "true"
        else:
            confidence = prob[0] * 100
            result = f"FAKE NEWS ❌ ({confidence:.0f}% Confident)"
            result_type = "fake"
            
        return render_template('index.html', result=result, result_type=result_type, 
                               original=original_text, translated=translated_display, confidence=confidence)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)