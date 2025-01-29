import unittest
import time
from src.rag.query_service import QueryService

class TestQueryService(unittest.TestCase):
    def setUp(self):
        self.service = QueryService()
        self.index_name = "documents"
        self.service.es_handler.create_index(
            index_name=self.index_name,
            mappings={
                "mappings": {
                    "properties": {
                        "ticker": {"type": "keyword"},
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "type": {"type": "keyword"},
                        "published_date": {"type": "date"},
                        "url": {"type": "keyword"},
                    }
                }
            }
        )
        # Index sample documents
        self.service.es_handler.index_document(
            self.index_name,
            "doc1",
            {
                "ticker": "NVDA",
                "title": "Earnings Call",
                "content": "NVIDIA announces new GPUs and record earnings. The company expects to launch new products in the coming months. The CEO discussed the company's growth strategy and future plans.",
                "type": "transcript",
                "published_date": "2023-01-01",
                "url": "http://example.com/1"
            }
        )
        self.service.es_handler.index_document(
            self.index_name,
            "doc2",
            {
                "ticker": "NVDA",
                "title": "News Article",
                "content": "NVIDIA faces operational risks due to supply chain issues.",
                "type": "news",
                "published_date": "2023-02-01",
                "url": "http://example.com/2"
            }
        )
        time.sleep(1)  # Allow time for the documents to index

    def test_search_documents(self):
        results = self.service.search_documents("NVDA", "record earnings")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["ticker"], "NVDA")
        self.assertIn("record earnings", results[0]["excerpt"].lower())

    def tearDown(self):
        self.service.es_handler.es.options(ignore_status=[400,404]).indices.delete(index=self.index_name)

if __name__ == "__main__":
    unittest.main()
