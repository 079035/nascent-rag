import logging
import nltk
from sentence_transformers import SentenceTransformer
from src.pipeline.transcript_fetcher import fetch_transcripts
from src.pipeline.news_fetcher import fetch_news
from src.rag.elasticsearch_handler import ElasticsearchHandler
from src.rag.query_service import QueryService
from nltk.tokenize import sent_tokenize

logging.basicConfig(level=logging.INFO)

def process_sentence_pairs(sentences):
        paired_sentences = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences):
                pair = f"{sentences[i]} {sentences[i+1]}"
                paired_sentences.append(pair)
                i += 2
            else:
                paired_sentences.append(sentences[i])  # Last sentence alone if odd
                i += 1
        return paired_sentences

def main():
    # Initialize Elasticsearch handler
    handler = ElasticsearchHandler()
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Using a lightweight embedding model
    nltk.download('punkt_tab')

    # Create index if not exists
    handler.create_index(
        index_name="documents",
        mappings={
            "mappings": {
                "properties": {
                    "ticker": {"type": "keyword"},
                    "title": {"type": "text"},
                    "sentence": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 384},
                    "type": {"type": "keyword"},
                    "published_date": {"type": "date"},
                    "url": {"type": "keyword"},
                }
            }
        }
    )
    
    # Fetch and index data
    tickers = ["NVDA", "TSLA", "AMZN", "XOM", "JNJ", "DE"]
    logging.info("Fetching transcripts and news articles...")
    transcripts = fetch_transcripts(tickers, 8)
    articles = fetch_news(tickers, 20)

    logging.info("Indexing documents with sentence embeddings...")
    
    # Process and index documents
    for ticker, transcript_data in transcripts.items():
        for transcript in transcript_data:
            sentences = sent_tokenize(transcript.get("attributes", "").get("content", ""))  # Sentence split using tokenizer
            sentence_pairs = process_sentence_pairs(sentences)
            for sentence_pair in sentence_pairs:
                embedding = model.encode(sentence_pair).tolist()
                document = {
                    "ticker": ticker,
                    "title": transcript.get("attributes", None).get("title", ""),
                    "sentence": sentence_pair,
                    "embedding": embedding,
                    "type": "transcript",
                    "published_date": transcript.get("attributes", None).get("publishOn", None),
                    "url": transcript.get("links", None).get("canonical", "")
                }
                doc_id = f"transcript-{ticker}-{hash(sentence_pair)}"
                handler.index_document(index_name="documents", doc_id=doc_id, document=document)

    for ticker, news_data in articles.items():
        for article in news_data:
            sentences = sent_tokenize(article.get("attributes", "").get("content", ""))  # Sentence split using tokenizer
            sentence_pairs = process_sentence_pairs(sentences)
            for sentence_pair in sentence_pairs:
                embedding = model.encode(sentence_pair).tolist()
                document = {
                    "ticker": ticker,
                    "title": article.get("attributes", None).get("title", ""),
                    "sentence": sentence_pair,
                    "embedding": embedding,
                    "type": "news",
                    "published_date": article.get("attributes", None).get("publishOn", None),
                    "url": article.get("links", None).get("canonical", "")
                }
                doc_id = f"news-{ticker}-{hash(sentence_pair)}"
                handler.index_document(index_name="documents", doc_id=doc_id, document=document)
    
    logging.info("Finished indexing documents.")
    
    # Initialize query service
    query_service = QueryService()
    
    # Interactive user input
    while True:
        ticker = input("Enter stock ticker (or 'exit' to quit): ").strip().upper()
        if ticker.lower() == 'exit':
            handler.delete_index(index_name="documents")
            break
        query = input("Enter your query: ").strip()
        query_embedding = model.encode(query).tolist()
        results = query_service.search_documents_by_embedding(ticker=ticker, query_embedding=query_embedding, max_results=2)
        
        if results:
            print("\nRelevant Results:")
            for res in results:
                print(f"Title: {res['title']}")
                print(f"Score: {res['score']}")  # Cosine similarity score
                print(f"Excerpt: {res['sentence']}")  # Relevant sentence
                print(f"Published Date: {res['published_date']}")  # Date of publication
                print(f"URL: {res['url']}")
                print("-" * 80)
        else:
            print("No relevant results found.")

if __name__ == "__main__":
    main()
