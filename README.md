# StructDiff

Determine the relative structure of different websites using vector based search

:construction: _Work in Progress_ :construction:

## What and Why

This service scrapes, classifies and ranks websites by their structural similarity, allowing you to discover sites with comparable HTML patterns. It provides two main endpoints;

- The `/process` endpoint is needed to input a vector representation of the site's HTML. Provide a list of URLs to input into the service
- The `/similarity` endpoint is where similarity search is happens. Provide a URL as a query parameter, and this endpoint shows how structurally similar all sites previously inputted using the process endpoint

The API spec for each endpoint is provided as a [Bruno Collection](./docs/bruno).

## Local setup

1. Spin up a weaviate instance using your local Docker

```bash
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.29.2
```

2. Setup the virtual environment with dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

2. Download the required NLP model using the script

```bash
python3 scripts/save_model.py
```

3. Start the server on your local machine with required config

```bash
cp .env.example .env
python3 wsgi.py
```

## Tooling

Unit tests and linting can be run locally as follows;

```bash
pip3 install -r dev-requirements
pytest
ruff check
```
