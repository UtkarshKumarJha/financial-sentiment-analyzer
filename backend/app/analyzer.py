# analyzer.py
import requests
from bs4 import BeautifulSoup

def get_article_content(url: str) -> str | None:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return content.strip() if content else None

    except Exception as e:
        print(f"[ERROR] Could not fetch article from {url}: {e}")
        return None
