import unittest
from src.pipeline.news_fetcher import fetch_news

class TestNewsFetcher(unittest.TestCase):
    def test_fetch_news(self):
        tickers = ["NVDA", "TSLA"]
        articles = fetch_news(tickers)
        self.assertIsInstance(articles, dict)
        self.assertIn("NVDA", articles)
        self.assertIn("TSLA", articles)
        self.assertGreater(len(articles["NVDA"]), 0)

if __name__ == "__main__":
    unittest.main()
