# Nascent RAG Project

```
nascent-rag/
│
├── src/
│   ├── pipeline/                       # Code for pulling and processing documents
│   │   ├── __init__.py
│   │   ├── transcript_fetcher.py
│   │   └── news_fetcher.py
│   ├── query_service/                  # Code for querying documents
│   │   ├── __init__.py
|   |   ├── elasticsearch_handler.py    # Functions for interacting with Elasticsearch
│   │   └── query_service.py            # RAG querying service
│   └── utils/                          # Utility scripts
│       ├── __init__.py
│       └── logger.py
│
├── tests/                              # Test scripts
│   ├── test_pipeline.py
│   └── test_query_service.py
│
├── requirements.txt                    # Dependency management
├── README.md                           # Instructions for running the project
├── Dockerfile                          # Dockerfile for containerization
└── .gitignore                          # Files and directories to ignore in the repo
```
