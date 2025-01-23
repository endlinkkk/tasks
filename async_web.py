import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def async_web_server(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:

                status = response.status
                print("Status:", response.status)
        except ClientConnectionError:
            status = 0

    return status


async def fetch_urls(urls: list[str], file_path: str):
    tasks = [async_web_server(url) for url in urls]
    result = await asyncio.gather(*tasks)
    for url, result in zip(urls, result):  # noqa: B020
        print({f"url: {url}, status_code: {result}"})



if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
