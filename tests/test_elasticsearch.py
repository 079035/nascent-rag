import unittest
import time
from src.rag.elasticsearch_handler import ElasticsearchHandler

class TestElasticsearchHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ElasticsearchHandler()
        self.index_name = "test_documents"
        self.handler.create_index(
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

    def test_index_document(self):
        document = {
            "ticker": "NVDA",
            "title": "Earnings Call",
            "content": "NVIDIA announces record earnings...",
            "type": "transcript",
            "published_date": "2023-01-01",
            "url": "http://example.com"
        }
        self.handler.index_document(self.index_name, "test-doc-1", document)
        time.sleep(1)  # Allow time for the document to index
        query={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"ticker": "NVDA"}}  # Ensure ticker matches exactly
                    ]
                }
            }
        }
        result = self.handler.search(self.index_name, query)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]["_source"]["ticker"], "NVDA")

    def tearDown(self):
        self.handler.es.options(ignore_status=[400,404]).indices.delete(index=self.index_name)

if __name__ == "__main__":
    unittest.main()
