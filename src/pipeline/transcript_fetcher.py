import requests
import logging
import os
from collections import defaultdict
from typing import List

BASE_URL = "https://seeking-alpha.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
	"x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
}

logging.basicConfig(level=logging.INFO)

def fetch_transcripts(tickers: List[str], num_transcripts: int = 20) -> dict:
    """
    Fetch earnings call transcripts for a list of stock tickers.
    
    Args:
        tickers (List[str]): List of stock tickers (e.g., ["NVDA", "TSLA"]).

    Returns:
        dict: Dictionary of transcripts indexed by ticker.
    """
    transcripts = defaultdict(list) # ticker -> transcript data
    for ticker in tickers:
        try:
            transcript_ids = []
            url = f"{BASE_URL}/transcripts/v2/list"
            params = {"id":ticker,"size":num_transcripts,"number":"1"}
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            for i in range(num_transcripts):
                transcript_ids.append(response.json()["data"][i]["id"])  # Transcript ID for the ticker
            logging.info(f"Fetched transcript for {ticker}")
        except Exception as e:
            logging.error(f"Failed to fetch transcript for {ticker}: {e}")
        try:
            for transcript_id in transcript_ids:
                url = f"{BASE_URL}/transcripts/v2/get-details"
                params = {"id":transcript_id}
                response = requests.get(url, headers=HEADERS, params=params)
                response.raise_for_status()
                transcripts[ticker].append(response.json()["data"])  # Transcript details for the ticker
        except Exception as e:
            logging.error(f"Failed to fetch transcript details for {ticker}: {e}")
        # break

    return transcripts

if __name__ == "__main__":
    tickers = ["NVDA", "TSLA", "AMZN", "XOM", "JNJ", "DE"]
    transcripts = fetch_transcripts(tickers)
    for ticker, transcript_list in transcripts.items():
        print(f"Transcripts for {ticker}:")
        for transcript in transcript_list:
            print(f"Title: {transcript['attributes']['title']}")
            print(f"Published Date: {transcript['attributes']['publishOn']}")
            print(f"URL: {transcript['links']['canonical']}")
            print()
