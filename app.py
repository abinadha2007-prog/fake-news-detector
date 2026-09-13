from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# --- ML Model Training ---
# Real and Fake news samples to train
real_news_samples = [
    "ISRO successfully launched Aditya L1 to study the Sun",
    "Chennai Metro Rail second phase construction is progressing",
    "India won the Cricket World Cup in 2011",
    "Prime Minister inaugurated new parliament building in Delhi",
    "Tamil Nadu government announces new schools in rural areas",
    "Scientists discovered water on Moon by Chandrayaan mission",
    "Indian economy grows at 7 percent this year",
    "Chennai Super Kings won IPL trophy",
    "ISRO Aditya L1 reached its destination",
    "Election Commission announces election dates",
    "இஸ்ரோ ஆதித்யா எல்1 விண்கலத்தை வெற்றிகரமாக செலுத்தியது",
    "சென்னை மெட்ரோ ரயில் இரண்டாம் கட்ட பணிகள் நடைபெற்று வருகின்றன"
]

fake_news_samples = [
    "NASA confirms Earth will experience 5 days of darkness",
    "Government announces free laptop and 1 lakh cash if you forward this message",
    "Drinking 10 liters of water makes you immortal scientists found",
    "WhatsApp will charge 5 rupees per message share to 10 groups",
    "Drink lemon honey cures all cancer in 7 days miracle cure",
    "Free money click here to win lottery prize",
    "Aliens landed in Chennai shocking news",
    "Earth will end tomorrow NASA confirms",
    "நாசா உறுதிப்படுத்தியது 5 நாட்கள் இருட்டில் இருக்கும்",
    "இந்த மெசேஜை 10 குழுவிற்கு பகிரவும் இல்லையெனில் வாட்ஸ்அப் கட்டணம்",
    "தினமும் இதை குடித்தால் புற்றுநோய் 7 நாளில் குணமாகும் அதிர்ச்சி"
]

# Training
all_texts = real_news_samples + fake_news_samples
all_labels = [1] * len(real_news_samples) + [0] * len(fake_news_samples) # 1=Real, 0=Fake

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_texts)
model = LogisticRegression()
model.fit(X, all_labels)

def predict_fake_news(text):
    if len(text.split()) < 4:
        return "Please enter more complete news", 0

    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    confidence = int(max(prob) * 100)

    if pred == 1:
        return "REAL NEWS - This news appears to be Real", confidence
    else:
        return "FAKE NEWS - This news appears to be Fake", confidence

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
