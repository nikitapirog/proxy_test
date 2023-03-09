import asyncio
from functools import partial

import pytest
import requests

proxies = {
    'http': 'http://0.0.0.0:80',
    'https': 'http://0.0.0.0:80'
}


@pytest.mark.asyncio
async def test_response_200_connected(server):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, partial(requests.get, url='http://0.0.0.0:8000', proxies=proxies))
    assert response.status_code == 200
    assert list(response.iter_lines())[0] == b'HTTP/1.1 200 I am happy to see you again'


@pytest.mark.asyncio
async def test_response_666_code(server):
    headers = {'User-Agent': 'Netscape'}
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, partial(requests.get, url='http://0.0.0.0:8000', proxies=proxies,
                                                        headers=headers))
    assert response.status_code == 666
