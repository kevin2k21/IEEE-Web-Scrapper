import httpx
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from loguru import logger

class BaseScraper(ABC):
    """
    Abstract Base Class for all IEEE opportunity scrapers.

    Provides common functionality for making asynchronous HTTP requests
    with built-in exponential backoff and retries via tenacity. All
    concrete scraper implementations must inherit from this class and
    implement the `source_name`, `start_url`, and `parse` methods.

    Attributes:
        headers (Dict[str, str]): Default HTTP headers for requests.
        timeout (httpx.Timeout): Default timeout configuration.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.timeout = httpx.Timeout(15.0)

    @property
    @abstractmethod
    def source_name(self) -> str:
        """
        Name of the source (e.g., 'ieee_cs_cfp').
        Used for logging and database tracking.
        """
        pass

    @property
    @abstractmethod
    def start_url(self) -> str:
        """
        The initial URL to scrape.
        """
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def fetch(self, url: str, **kwargs) -> httpx.Response:
        """Fetch a URL with retries and exponential backoff"""
        logger.info(f"Fetching {url} for {self.source_name}")
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response

    @abstractmethod
    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        """Parse the response and return a list of raw opportunity dictionaries"""
        pass

    async def scrape(self) -> List[Dict[str, Any]]:
        """Main entry point to run the scraper"""
        try:
            response = await self.fetch(self.start_url)
            results = await self.parse(response)
            logger.info(f"Scraper {self.source_name} finished. Found {len(results)} records.")
            return results
        except Exception as e:
            logger.error(f"Scraper {self.source_name} failed: {e}")
            raise
