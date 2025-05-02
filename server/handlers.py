from asyncio import gather
from dataclasses import dataclass
from typing_extensions import Optional
from fastapi import APIRouter, HTTPException
from transformers import MarkupLMProcessor, MarkupLMModel
import numpy as np
import logging

from .scrape import scrape_site
from .weaviate import store_embeddings, vector_search


MAX_SCRAPES = 10
DEFAULT_SITE_TIMESTAMP = 20250101000000000000
MODEL_PATH = "./models/saved_markup_model"
PROCESSOR_PATH = "./models/saved_markup_processor"

router = APIRouter(prefix="/api")


@dataclass
class ProcessRequest:
    urls: list[str]
    timestamp: Optional[int] = None


@router.post("/process")
async def process_handler(req: ProcessRequest) -> dict:
    """Route for scraping and profiling the urls provided"""
    if len(req.urls) > MAX_SCRAPES:
        logging.info("Client error at /api/process")
        raise HTTPException(
            status_code=400,
            detail=f"Can process a max of {MAX_SCRAPES} urls concurrently",
        )

    timestamp = req.timestamp or DEFAULT_SITE_TIMESTAMP
    scrapes = await gather(*[scrape_site(url, timestamp) for url in req.urls])
    logging.info("Sites scraped")

    processor = MarkupLMProcessor.from_pretrained(PROCESSOR_PATH)
    model = MarkupLMModel.from_pretrained(MODEL_PATH)
    inputs = [processor(scrape, return_tensors="pt") for scrape in scrapes]
    encodings = [model(**input) for input in inputs]
    logging.info("Encodings generated")

    embeddings_dict = {
        url: np.array(encoding).tolist() for url, encoding in zip(req.urls, encodings)
    }
    store_embeddings(embeddings_dict)

    return {"message": "success"}


@router.get("/similarity")
async def search_handler(url: str, timestamp: Optional[int] = None) -> dict:
    """Route for finding the most similar urls to the one provided"""
    scrape = await scrape_site(url, timestamp or DEFAULT_SITE_TIMESTAMP)
    logging.info("Site scraped")

    processor = MarkupLMProcessor.from_pretrained(PROCESSOR_PATH)
    model = MarkupLMModel.from_pretrained(MODEL_PATH)
    input = processor(scrape, return_tensors="pt")
    encoding = model(**input)
    logging.info("Encoding generated")

    embedding = np.array(encoding).tolist()
    urls = vector_search(embedding)

    return {"similar_urls": urls}
