def predict_fake_news(text):
    text_lower = text.lower()
    fake_keywords = ["nasa confirms darkness", "5 days of darkness", "drink 10 liters immortal", "shocking", "miracle cure", "click here to win", "free money"]
    
    fake_score = 0
    for word in fake_keywords:
        if word in text_lower:
            fake_score += 2
            
    if len(text.split()) < 4:
        return "Please enter more text", 0

    if fake_score >= 1:
        return "FAKE NEWS - This news appears to be Fake", 95
    else:
        return "REAL NEWS - This news appears to be Real", 92
