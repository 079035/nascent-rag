import requests
import logging
import os
from time import sleep
from typing import List
from collections import defaultdict

BASE_URL = "https://seeking-alpha.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}

logging.basicConfig(level=logging.INFO)

def get_single_article(article_id: str) -> dict:
    """
    Fetch a single news article by ID.
    
    Args:
        article_id (str): Seeking Alpha article ID.

    Returns:
        dict: Dictionary of article details.
    """
    article = {}
    try:
        url = f"{BASE_URL}/news/get-details"
        params = {"id":article_id}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        article = response.json()['data']  # JSON response for the article
        logging.info(f"Fetched article {article_id}")
    except Exception as e:
        logging.error(f"Failed to fetch article {article_id}: {e}")
    
    return article

def fetch_news(tickers: List[str], num_articles: int = 20) -> dict:
    """
    Fetch recent news articles for a list of stock tickers.
    
    Args:
        tickers (defaultdict(str)): List of stock tickers (e.g., ["NVDA", "TSLA"]).
        num_articles (int): Number of recent articles to fetch for each ticker.

    Returns:
        dict: Dictionary of articles indexed by ticker.
    """
    article_list = {}
    articles = defaultdict(list) # ticker -> article data
    for ticker in tickers:
        try:
            url = f"{BASE_URL}/news/v2/list-by-symbol"
            params = {"size":num_articles,"number":"1","id":ticker}
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            article_list = response.json()  # JSON response for the ticker
            logging.info(f"Fetched {num_articles} latest articles for ticker {ticker}")
        except Exception as e:
            logging.error(f"Failed to fetch latest articles for ticker {ticker}: {e}")
        try:
            for article_idx in range(len(article_list["data"])):
                article_id = article_list["data"][article_idx]["id"]
                articles[ticker].append(get_single_article(article_id))
                sleep(5)
            logging.info(f"Fetched article details for ticker {ticker}")
        except Exception as e:
            logging.error(f"Failed to fetch article details for ticker {ticker}: {e}")

    return articles

if __name__ == "__main__":
    pass
