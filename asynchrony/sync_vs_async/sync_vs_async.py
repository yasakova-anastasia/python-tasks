import aiohttp
import asyncio
import requests
import multiprocessing
from functools import partial


async def async_fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Asyncronously fetch (get-request) single url using provided session
    :param session: aiohttp session object
    :param url: target http url
    :return: fetched text
    """
    async with session.get(url) as resp:
        response = await resp.read()
    return response.decode()


async def async_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls using aiohttp
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(async_fetch(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    return responses


def sync_fetch(session: requests.Session, url: str) -> str:
    """
    Syncronously fetch (get-request) single url using provided session
    :param session: requests session object
    :param url: target http url
    :return: fetched text
    """
    with session.get(url) as resp:
        response = resp.content
    return response.decode()


def threaded_requests(urls: list[str]) -> list[str]:
    """
    Concurrently fetch provided urls with requests in different threads
    :param urls: list of http urls ot fetch
    :return: list of fetched texts
    """
    with requests.Session() as session:
        with multiprocessing.Pool() as pool:
            result = pool.map(partial(sync_fetch, session), urls)
    return result
