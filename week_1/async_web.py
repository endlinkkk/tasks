import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
]

sem = asyncio.Semaphore(5)


async def async_web_server(url: str, session: aiohttp.ClientSession) -> int:
    async with sem:
        try:
            async with session.get(url) as response:
                status = response.status
        except ClientConnectionError:
            status = 0
    return status


async def fetch_urls(urls: list[str], file_path: str):
    async with aiohttp.ClientSession() as session:
        tasks = [async_web_server(url, session) for url in urls]
        results = await asyncio.gather(*tasks)

    for url, result in zip(urls, results):  # noqa: B020
        print({f"url: {url}, status_code: {result}"})


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "./results.jsonl"))
