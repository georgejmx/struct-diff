from httpx import AsyncClient
from bs4 import BeautifulSoup


RELEVANT_TAGS = [
    "header",
    "footer",
    "main",
    "nav",
    "section",
    "article",
    "aside",
    "div",
    "h1",
    "h2",
    "h3",
    "p",
    "ul",
    "ol",
    "li",
    "blockquote",
    "a",
    "img",
    "video",
    "audio",
    "iframe",
    "form",
    "input",
    "button",
    "select",
    "textarea",
]


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
    body = soup.find("body")

    if not body:
        raise Exception(
            f"Site with url {url} cannot be parsed or has severely malformed HTML"
        )

    text_tags = [
        tag.name for tag in body.find_all(lambda tag: tag.name in RELEVANT_TAGS)
    ]
    return " ".join(text_tags)
