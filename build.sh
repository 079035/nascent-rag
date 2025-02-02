#!/bin/bash

docker-compose down

docker-compose up --build -d elasticsearch

echo "Waiting for Elasticsearch to start..."
sleep 10

docker-compose run rag-app
