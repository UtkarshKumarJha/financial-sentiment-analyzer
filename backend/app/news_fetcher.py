# fetch_news.py
import yfinance as yf

def fetch_news(ticker_symbol="AAPL", limit=10):
    try:
        ticker = yf.Ticker(ticker_symbol)
        raw_news = ticker.news
    except Exception as e:
        print(f"[ERROR] Could not fetch news for {ticker_symbol}: {e}")
        return []

    data = []

    for article in raw_news[:limit]:
        try:
            content = article.get("content", {})
            data.append({
                "title": content.get("title", ""),
                "url": content.get("canonicalUrl", {}).get("url", ""),
                "publishedAt": content.get("pubDate", ""),
                "source": content.get("providerPublishTime", ""),  # optional
                "ticker": ticker_symbol
            })
        except Exception as e:
            print(f"[WARN] Skipping article due to error: {e}")
            continue

    return data
