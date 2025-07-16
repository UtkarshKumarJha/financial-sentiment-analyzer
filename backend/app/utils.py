from datetime import datetime
import json
from .analyzer import get_article_content
from .sentiment import finbert_sentiment
from .news_fetcher import fetch_news


def analyze_articles(ticker = "AAPL"):
    
    articles = fetch_news(ticker)

    results = []
    for article in articles:
        content = get_article_content(article["url"])
        if not content or len(content) < 200:
            print(f"[SKIP] Short or no content for: {article['title']}")
            continue

        sentiment, confidence = finbert_sentiment(content)

        article["sentiment"] = sentiment
        article["confidence"] = confidence
        article["timestamp"] = datetime.now().isoformat()
        results.append(article)
        
    return results