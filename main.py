import requests
import json
from datetime import datetime
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from bs4 import BeautifulSoup
from textblob import TextBlob
import yfinance as yf

# API_KEY = "6ef7b5065aca46b8a7851eb6c6eb9bd6"
# COMPANIES = ["Google", "Microsoft", "Facebook", "Netflix", "Apple", "Amazon", "Tesla", "Nvidia", "AMD", "Intel"]

nlp = spacy.load("en_core_web_sm")

# Optional: Keep FinBERT if needed
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# -------------------------------
# FETCHING NEWS
# -------------------------------
def fetch_news():
    # for company in COMPANIES:
    #     url = f"https://newsapi.org/v2/top-headlines?q={company}&language=en&pageSize=5&sortBy=publishedAt&apiKey={API_KEY}"
    #     response = requests.get(url)
    #     data = response.json()
    #     if data.get('status') == 'ok':
    #         with open(f'{company.lower().replace(" ", "_")}_news.json', 'w') as file:
    #             json.dump(data['articles'], file, indent=4)
    news = yf.Ticker("AAPL").news
    data = []
    for article in news:
        
    # Save Apple news to a file
    with open('apple_news.json', 'w') as file:
        json.dump(data, file, indent=4)

# -------------------------------
# LOAD ARTICLES
# -------------------------------
def load_articles():
    articles = []
    for company in COMPANIES:
        try:
            with open(f'{company.lower().replace(" ", "_")}_news.json', 'r') as file:
                data = json.load(file)
                for article in data:
                    if 'title' in article and 'url' in article:
                        articles.append({
                            'company': company,
                            'title': article['title'],
                            'link': article['url'],
                            'timestamp': datetime.now().isoformat()
                        })
        except FileNotFoundError:
            print(f"No news file found for {company}. Skipping.")
    
    with open('articles.json', 'w') as file:
        json.dump(articles, file, indent=4)

# -------------------------------
# GET FULL ARTICLE CONTENT USING BEAUTIFULSOUP
# -------------------------------
def get_article_content(link):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to extract <p> tags and join them
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content.strip()
    except Exception as e:
        print(f"[ERROR] Could not fetch article from {link}: {e}")
        return None

# -------------------------------
# TEXTBLOB SENTIMENT
# -------------------------------
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment, polarity

# -------------------------------
# ANALYZE ALL ARTICLES
# -------------------------------
def analyze_articles():
    with open('articles.json', 'r') as file:
        articles = json.load(file)
    
    results = []
    for article in articles:
        content = get_article_content(article["link"])
        if not content or len(content) < 200:
            print(f"[SKIP] Short or no content for: {article['title']}")
            continue

        sentiment, polarity = get_sentiment(content)
        article["sentiment"] = sentiment
        article["sentiment_polarity"] = round(polarity, 3)
        article["timestamp"] = datetime.now().isoformat()
        results.append(article)

    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)

# -------------------------------
# MAIN ENTRY
# -------------------------------
if __name__ == "__main__":
    fetch_news()
    # load_articles()
    # analyze_articles()
    # print("✅ Analysis complete. Check results.json")
