from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import logging

from .handlers import router as api_router
from .weaviate import setup_collection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handler to isomorphically initialise the weaviate collection for dev purposes"""
    setup_collection()
    logging.info("Weaviate collection verified")
    yield


load_dotenv()
app = FastAPI(
    title="StructDiff",
    summary="Determine the relative structure of websites using vector based search",
    lifespan=lifespan,
)


@app.get("/health", response_class=PlainTextResponse)
def health_controller() -> str:
    logging.info("Call to /health")
    return "Healthy"


app.include_router(api_router)
