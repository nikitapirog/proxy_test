import asyncio

import pytest

from proxy import create_server_tasks


@pytest.fixture()
def server(event_loop):
    cancel_handle = asyncio.ensure_future(create_server_tasks(event_loop), loop=event_loop)
    event_loop.run_until_complete(asyncio.sleep(0.01))
    try:
        yield
    finally:
        cancel_handle.cancel()
