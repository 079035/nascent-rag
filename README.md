# Nascent RAG Application

This project provides a **Retrieval-Augmented Generation (RAG)** pipeline using an Elasticsearch backend and sentence-based embedding search.


## Setup Instructions

### Requirements
- Docker and Docker Compose installed

### Environment Variables
You need to provide the **RAPIDAPI_KEY** for accessing Seeking Alpha’s API. You can do this by using a `.env` file or exporting it directly.

### Steps to Build and Run the Project
1. Clone this repository:
    ```bash
    git clone https://github.com/079035/nascent-rag
    cd nascent-rag
    ```
2. Create a `.env` file in the project root directory:
    ```bash
    RAPIDAPI_KEY=your_actual_rapidapi_key_here
    ```
3. Build and start the application using the provided script:
    ```bash
    sh build.sh
    ```
4. Verify that the containers are running:
    ```bash
    docker ps
    ```


## Running the Application
The application runs interactively in the terminal, prompting for a stock ticker and query.

Example:
```bash
Enter stock ticker (or 'exit' to quit): NVDA
Enter your query: product launches
```
