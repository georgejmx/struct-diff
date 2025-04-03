from httpx import AsyncClient
from bs4 import BeautifulSoup


async def fetch_site(url: str, timestamp: int) -> str:
    """Call the Wayback Machine for raw html at the given timestamp"""
    async with AsyncClient() as client:
        wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
        response = await client.get(wayback_url)
        return response.text

async def scrape_site(url: str, timestamp: int) -> str:
    """Scrapes a single site given a timestamp and its raw html"""
    html = await fetch_site(url, timestamp)
    soup = BeautifulSoup(html, "html.parser")

    text_tags = [tag.name for tag in soup.find_all()]
    return " ".join(text_tags)
