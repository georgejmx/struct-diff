from httpx import AsyncClient

HTML_START = "<body"
HTML_END = "</body>"


async def fetch_site(url: str, timestamp: int) -> str:
    """Call the Wayback Machine for raw html at the given timestamp"""
    async with AsyncClient() as client:
        wayback_url = f"https://web.archive.org/web/{url}"
        response = await client.get(wayback_url)
        return response.content.decode('utf-8', errors='ignore')


def extract_body(html: str) -> str | None:
    start_marker_index = html.find(HTML_START)
    if start_marker_index == -1:
        return None

    start_index = html.find('>', start_marker_index) + 1
    end_index = html.find(HTML_END)
    if end_index == -1:
        return None

    return html[start_index:end_index]

async def scrape_site(url: str, timestamp: int) -> str:
    """Scrapes a single site given a timestamp and its raw html"""
    html = await fetch_site(url, timestamp)
    body_html = extract_body(html)

    if not body_html:
        raise Exception(
            f"Site with url {url} cannot be parsed or has severely malformed HTML"
        )

    return body_html
