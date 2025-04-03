# StructDiff

Determine the relative structure of different websites using vector based search

:construction: _Work in Progress_ :construction:

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
deactivate
```
