import json

from aiohttp import ClientSession, web


async def handle(request: web.Request) -> web.Response:
    currency = request.match_info.get('currency', "USD")

    async with ClientSession() as session:
        print(f'https://api.exchangerate-api.com/v4/latest/{currency}')
        async with session.get(f'https://api.exchangerate-api.com/v4/latest/{currency}') as response:
            data = await response.json()
    return web.Response(text=json.dumps(data))

async def my_web_app():
    app = web.Application()
    app.add_routes([web.get('/', handle),
                web.get('/{currency}', handle)])
    return app
