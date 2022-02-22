import aiohttp


class HttpUtils:

    @staticmethod
    async def send(method: str, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, ssl=False) as response:
                return response.status, await response.read()
