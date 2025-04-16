from os import getenv
from weaviate import connect_to_local
from weaviate.client import WeaviateClient
from weaviate.classes.config import Property, DataType
import logging


COLLECTION_NAME = "SiteStructures"


def _get_client() -> WeaviateClient:
    return connect_to_local(
        host=getenv("WEAVIATE_HOST"), port=int(getenv("WEAVIATE_PORT"))
    )


def setup_collection():
    with _get_client() as client:
        if not client.collections.exists(COLLECTION_NAME):
            client.collections.create(
                name=COLLECTION_NAME,
                vectorizer_config=None,
                properties=[Property(name="url", data_type=DataType.TEXT)],
            )


def store_embeddings(embeddings: dict[str, list[int]]):
    """Send embeddings to weviate"""
    failed_retrievals = None

    with _get_client() as client:
        collection = client.collections.get(COLLECTION_NAME)

        with collection.batch.dynamic() as batch:
            for k, v in embeddings.items():
                batch.add_object(properties={"url": k}, vector=v)

        failed_retrievals = collection.batch.failed_objects

    if failed_retrievals:
        logging.error(f"Number of failed imports: {len(failed_retrievals)}")
        logging.error(f"First failed object: {failed_retrievals[0]}")


def vector_search(vector: list[int], count: int = 5) -> list[str]:
    """Lookup which entries in the collection are most similar"""
    sites: list[str] = []

    with _get_client() as client:
        collection = client.collections.get(COLLECTION_NAME)

        results = collection.query.near_vector(
            near_vector=vector, limit=count, return_properties=["url"]
        )

        for result in results.objects:
            sites.append(result.properties["url"])

    return sites
