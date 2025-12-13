"""Scrapy spider to scrape alll the links reachable from a website."""

from collections.abc import AsyncGenerator, Generator

import scrapy
from scrapy.http import Response

PLAYWRIGHT_PARAMS = {
    "playwright": True,
    "playwright_include_page": True,
}


class ComplexWebsiteLinksSpider(scrapy.Spider):
    """Spider to scrape all links from a complex website using Playwright."""

    name = "complex_website_links"
    handle_httpstatus_all = True

    visited_websites: set[str] = set()

    # Inline settings to ensure correct handler/middleware loading
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 600000,
    }

    def __init__(self, base_url: str | None = None, *args, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self._base_url = base_url or "http://localhost:3000"
        self.start_urls = [f"{self._base_url}/fr", f"{self._base_url}/en"]

    def start_requests(self) -> Generator[scrapy.Request]:
        """Generate initial requests to start scraping."""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta=PLAYWRIGHT_PARAMS)

    async def parse(self, response: Response) -> AsyncGenerator[dict]:
        """Parse a page and extract links."""
        self.logger.info(f"Parsing URL: {response.url}")

        # Use Playwright to render the page, scroll to load dynamic content and wait for it to load
        try:
            page = response.meta["playwright_page"]
            pages_errors = []
            page.on("pageerror", lambda err: pages_errors.append(err))
            # Wait for the page to load with a link
            await page.wait_for_selector("a")
            await page.wait_for_timeout(1000)
            # Scroll to the bottom of the page to load all content
            previous_height = None
            while True:
                current_height = await page.evaluate("() => document.body.scrollHeight")
                if previous_height == current_height:
                    break
                previous_height = current_height
                await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(300)
            self.logger.debug("Finished scrolling the page. Wait 10s")
            await page.wait_for_timeout(10000)
            html = await page.content()
        finally:
            await page.close()

        if pages_errors:
            self.logger.error(f"Parsing of the url stoped, page errors encountered: {pages_errors}")
            return

        # Extract all links
        sel = scrapy.Selector(text=html)
        links = sel.xpath("//a/@href").getall()
        for link in links:
            url = response.urljoin(link)
            if url.startswith(("mailto:", "tel:")):
                continue
            if url.startswith(self._base_url):
                if url.startswith(f"{self._base_url}/_nuxt"):
                    continue
                yield scrapy.Request(url, callback=self.parse, meta=PLAYWRIGHT_PARAMS)  # type: ignore[misc]
            elif url.rstrip("/") not in self.visited_websites:
                self.visited_websites.add(url.rstrip("/"))
                yield scrapy.Request(
                    url, callback=self._check_status, meta={"source_url": response.url}, dont_filter=True
                )  # type: ignore[misc]
            else:
                self.logger.debug(f"Already visited URL: {url}")
                yield {
                    "source_url": response.url,
                    "url": url,
                    "status": None,
                }

        # Parse the other pages by incrementing numerical parameters in the URL
        for new_url in self._generate_urls_to_parse(response.url):
            yield scrapy.Request(new_url, callback=self.parse, meta=PLAYWRIGHT_PARAMS)  # type: ignore[misc]

    def _check_status(self, response: Response) -> dict:
        """Check the status of an external link."""
        self.logger.info(f"Visiting URL: {response.url}")
        return {
            "source_url": response.meta["source_url"],
            "url": response.url,
            "status": response.status,
        }

    def _generate_urls_to_parse(self, url: str) -> Generator[str]:
        """Generate URLs to parse based by increasing parameter values."""
        start_index = 0
        while start_index != -1:
            start_index = url.find("=", start_index)
            if start_index == -1:
                break
            end_index = url.find("&", start_index)
            value = url[start_index + 1 : end_index]
            try:
                int(value)
            except ValueError:
                start_index += 1
                continue
            yield url[: start_index + 1] + str(int(value) + 1) + url[end_index:]
            start_index = end_index
