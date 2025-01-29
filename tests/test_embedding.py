import unittest
from sentence_transformers import SentenceTransformer
from src.rag.query_service import QueryService
from src.rag.elasticsearch_handler import ElasticsearchHandler

class TestQueryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up Elasticsearch index and populate it with test data.
        """
        cls.handler = ElasticsearchHandler()
        cls.query_service = QueryService()
        cls.index_name = "documents"
        cls.model = SentenceTransformer("all-MiniLM-L6-v2")  # Embedding model
        
        # Create index if it doesn't exist
        cls.handler.create_index(
            index_name=cls.index_name,
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

        # Sample documents
        test_data = [
            {
                "ticker": "NVDA",
                "title": "Earnings Call",
                "sentence": "NVIDIA announced record profits this quarter.",
                "embedding": cls.model.encode("NVIDIA announced record profits this quarter.").tolist(),
                "type": "transcript",
                "published_date": "2023-01-01",
                "url": "http://example.com/earnings"
            },
            {
                "ticker": "NVDA",
                "title": "Product Launch",
                "sentence": "NVIDIA unveiled a new AI-driven GPU today.",
                "embedding": cls.model.encode("NVIDIA unveiled a new AI-driven GPU today.").tolist(),
                "type": "news",
                "published_date": "2023-02-01",
                "url": "http://example.com/gpu"
            }
        ]

        # Insert test data into Elasticsearch
        for i, doc in enumerate(test_data):
            doc_id = f"test-doc-{i}"
            cls.handler.index_document(cls.index_name, doc_id, doc)
        import time
        time.sleep(2)  # Wait 2 seconds before querying

    def test_search_documents_by_embedding(self):
        """
        Test embedding-based search to ensure correct results are retrieved.
        """
        query = "NVIDIA profits"
        query_embedding = self.model.encode(query).tolist()

        results = self.query_service.search_documents_by_embedding(
            ticker="NVDA", query_embedding=query_embedding, max_results=2
        )

        self.assertGreater(len(results), 0, "No results found.")
        self.assertIn("NVIDIA", results[0]["sentence"], "Result does not contain expected content.")
        print("\nTest Results:")
        for res in results:
            print(f"Title: {res['title']}")
            print(f"Sentence: {res['sentence']}")
            print(f"Published Date: {res['published_date']}")
            print(f"URL: {res['url']}")
            print(f"Score: {res['score']}")
            print("-" * 80)

    @classmethod
    def tearDownClass(cls):
        """
        Delete the test index after tests complete.
        """
        cls.handler.es.options(ignore_status=[400, 404]).indices.delete(index=cls.index_name)

if __name__ == "__main__":
    unittest.main()
