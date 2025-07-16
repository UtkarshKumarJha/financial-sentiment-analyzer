from news_fetcher import fetch_news
from utils import analyze_articles

if __name__ == "__main__":
    fetch_news("AAPL")
    analyze_articles()