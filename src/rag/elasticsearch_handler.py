from elasticsearch import Elasticsearch
import logging
import time

logging.basicConfig(level=logging.INFO)

class ElasticsearchHandler:
    def __init__(self, host="http://elasticsearch:9200"):
        self.es = Elasticsearch(hosts=[host])
    
    def create_index(self, index_name: str, mappings: dict):
        """
        Create an Elasticsearch index with the given mappings.
        """
        if not self.es.indices.exists(index=index_name):
            self.es.options(ignore_status=[400,404]).indices.create(index=index_name, body=mappings)
            logging.info(f"Created index: {index_name}")
        else:
            logging.info(f"Index {index_name} already exists.")

    def index_document(self, index_name: str, doc_id: str, document: dict):
        """
        Index a single document in Elasticsearch.
        """
        self.es.index(index=index_name, id=doc_id, body=document)
        logging.info(f"Indexed document ID {doc_id} in {index_name}")

    def search(self, index_name: str, query: dict):
        """
        Perform a search query on an index.
        """
        response = self.es.search(index=index_name, body=query)
        return response['hits']['hits']

    def delete_index(self, index_name: str):
        """
        Delete an Elasticsearch index.
        """
        self.es.options(ignore_status=[400,404]).indices.delete(index=index_name)
        logging.info(f"Deleted index: {index_name}")

if __name__ == "__main__":
    pass
