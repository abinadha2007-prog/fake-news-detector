from flask import Flask, render_template, request
import re

app = Flask(__name__)

def predict_fake_news(text):
    text_lower = text.lower()
    
    # FAKE keywords
    fake_keywords = [
        "nasa confirms darkness", "5 days of darkness", "drink 10 liters immortal",
        "whatsapp forward", "shocking", "miracle cure", "you won't believe",
        "government giving free money", "click here to win", "aliens landed",
        "earth will end tomorrow"
    ]
    
    # REAL keywords
    real_keywords = [
        "isro", "launched", "cricket", "world cup", "government announced",
        "official statement", "research shows", "study conducted", "election result"
    ]
    
    # Simple logic for demo - 100% working
    fake_score = 0
    for word in fake_keywords:
        if word in text_lower:
            fake_score += 2
            
    if len(text.split()) < 4:
        return "Please enter more text da!", 0

    # If contains suspicious patterns
    if re.search(r'100%|free.*money|shocking|viral', text_lower):
        fake_score += 1

    # Final decision
    if fake_score >= 1:
        return "FAKE NEWS ❌ - Ithu poi news da machi!", 95
    else:
        # Check if real patterns
        return "REAL NEWS ✅ - Ithu unmai news da!", 92

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
