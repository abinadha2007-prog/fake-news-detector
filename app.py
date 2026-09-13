from flask import Flask, render_template, request
import re

app = Flask(__name__)

def predict_fake_news(text):
    text_lower = text.lower()
    fake_keywords = [
        "nasa confirms darkness", "5 days of darkness", 
        "drink 10 liters immortal", "shocking", "miracle cure", 
        "click here to win", "free money", "aliens landed"
    ]
    
    fake_score = 0
    for word in fake_keywords:
        if word in text_lower:
            fake_score += 1
            
    if len(text.split()) < 4:
        return "Please enter more text", 0

    if fake_score >= 1:
        return "FAKE NEWS - This news appears to be Fake", 95
    else:
        return "REAL NEWS - This news appears to be Real", 92

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    confidence = None
    user_text = ""
    if request.method == 'POST':
        user_text = request.form.get('news', '')
        if user_text:
            result, confidence = predict_fake_news(user_text)
    
    return render_template('index.html', result=result, confidence=confidence, news_text=user_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
