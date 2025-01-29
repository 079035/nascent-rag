from .elasticsearch_handler import ElasticsearchHandler
import logging
import nltk
from nltk.tokenize import sent_tokenize

logging.basicConfig(level=logging.INFO)

class QueryService:
    def __init__(self):
        self.es_handler = ElasticsearchHandler()
        self.index_name = "documents"

    def search_documents_by_embedding(self, ticker: str, query_embedding: list, max_results: int = 5):
        """
        Search for relevant documents based on an embedding similarity search.
        """
        search_query = {
            "size": max_results,
            "query": {
                "script_score": {
                    "query": {
                        "bool": {
                            "filter": [
                                {"term": {"ticker": ticker}}
                            ]
                        }
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }

        results = self.es_handler.search(self.index_name, search_query)

        excerpts = []
        for result in results:
            excerpts.append({
                "ticker": result["_source"]["ticker"],
                "title": result["_source"]["title"],
                "sentence": result["_source"]["sentence"],
                "published_date": result["_source"]["published_date"],
                "url": result["_source"]["url"],
                "score": result["_score"]
            })
        return excerpts

    def search_documents_by_keywords(self, ticker: str, query: str, max_results: int = 5):
        """
        Search for relevant documents based on the ticker and query.
        """
        search_query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": query}},
                        {"term": {"ticker": ticker}}
                    ]
                }
            },
            "size": max_results
        }

        results = self.es_handler.search(self.index_name, search_query)
        excerpts = []
        for result in results:
            content = result["_source"]["content"]
            # Extract relevant sentences
            sentences = sent_tokenize(content)
            relevant_sentences = [s for s in sentences if query.lower() in s.lower()]
            excerpts.append({
                "ticker": result["_source"]["ticker"],
                "type": result["_source"]["type"],
                "title": result["_source"]["title"],
                "published_date": result["_source"]["published_date"],
                "url": result["_source"]["url"],
                "excerpt": "\n- ".join(relevant_sentences),
                "score": result["_score"]
            })
        return excerpts

if __name__ == "__main__":
    pass
