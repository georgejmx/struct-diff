import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from server.scrape import scrape_site


TEST_TIMESTAMP = 1234567890


@pytest.fixture
def html_fixture() -> str:
    fixture_path = Path(__file__).parent / "__fixtures__" / "response.html"
    return fixture_path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_scrape_site(html_fixture):
    """Test scrape_site function with mocked fetch_site"""
    test_url = "https://example.co.uk"

    with patch("server.scrape.fetch_site", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = html_fixture

        result = await scrape_site(test_url, TEST_TIMESTAMP)

        mock_fetch.assert_called_once_with(test_url, TEST_TIMESTAMP)

        assert result =="<h1>test heading</h1><div><p>test paragraph</p></div>"


@pytest.mark.asyncio
async def test_scrape_broken_site():
    """Test scrape site function with mocked dodgy response from fetch_site"""
    test_url = "https://example.de"

    with patch("server.scrape.fetch_site", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = """<div class="hidden-content" style="display:none;">
        <script>document.write("Your browser security has been compromised!");</script>
        </div>"""

        with pytest.raises(Exception) as error:
            await scrape_site(test_url, TEST_TIMESTAMP)

        assert "https://example.de cannot be parsed" in str(error.value)
