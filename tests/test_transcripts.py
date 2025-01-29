import unittest
from src.pipeline.transcript_fetcher import fetch_transcripts

class TestTranscriptFetcher(unittest.TestCase):
    def test_fetch_transcripts(self):
        tickers = ["NVDA", "TSLA"]
        transcripts = fetch_transcripts(tickers)
        self.assertIsInstance(transcripts, dict)
        self.assertIn("NVDA", transcripts)
        self.assertIn("TSLA", transcripts)
        self.assertGreater(len(transcripts["NVDA"]), 0)

if __name__ == "__main__":
    unittest.main()
