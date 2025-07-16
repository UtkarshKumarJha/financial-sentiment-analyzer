# sentiment.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load FinBERT model and tokenizer once
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# VADER analyzer instance
vader_analyzer = SentimentIntensityAnalyzer()

def finbert_sentiment(text: str) -> dict:
    """
    Analyze sentiment using FinBERT.

    Returns:
        dict: { "sentiment": "positive|neutral|negative", "confidence": float }
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=1)
        sentiment_id = torch.argmax(probs).item()
        sentiment = ["negative", "neutral", "positive"][sentiment_id]
        confidence = probs[0][sentiment_id].item()
    return {
        "sentiment": sentiment,
        "confidence": round(confidence, 3)
    }

def vader_sentiment(text: str) -> str:
    """
    Analyze sentiment using VADER.

    Returns:
        str: "positive", "neutral", or "negative"
    """
    score = vader_analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    return "neutral"

def textblob_sentiment(text: str) -> str:
    """
    Analyze sentiment using TextBlob.

    Returns:
        str: "positive", "neutral", or "negative"
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"

def analyze_sentiment_all(text: str) -> dict:
    """
    Run all three models and return a combined sentiment analysis.
    """
    return {
        "textblob": textblob_sentiment(text),
        "vader": vader_sentiment(text),
        "finbert": finbert_sentiment(text)
    }

if __name__ == "__main__":
    sample = "Apple reported excellent quarterly results with revenue beating expectations."
    result = analyze_sentiment_all(sample)
    print(result)
