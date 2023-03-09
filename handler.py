import asyncio
from asyncio.streams import StreamReader, StreamWriter
from contextlib import closing
from typing import Tuple

import async_timeout

from http_parser import RawHTTPParser

StreamPair = Tuple[StreamReader, StreamWriter]


async def forward_stream(reader: StreamReader, writer: StreamWriter, event: asyncio.Event):
    while not event.is_set():
        try:
            data = await asyncio.wait_for(reader.read(1024), 1)
        except asyncio.TimeoutError:
            continue

        if data == b'':
            event.set()
            break

        writer.write(data)
        await writer.drain()


async def relay_stream(stream_pair_from: StreamPair, stream_pair_to: StreamPair):
    close_event = asyncio.Event()

    await asyncio.gather(
        forward_stream(*stream_pair_from, close_event),
        forward_stream(*stream_pair_to, close_event)
    )


async def https_handler(reader: StreamReader, writer: StreamWriter, request):
    remote_reader, remote_writer = await asyncio.open_connection('nginx', 80)
    with closing(remote_writer):
        writer.write(b'HTTP/1.1 200 Connection Established\r\n\r\n')
        await writer.drain()
        remote_writer.write(request)
        await remote_writer.drain()
        print('HTTP connection established')
        await relay_stream((reader, remote_writer), (remote_reader, writer))


async def main_handler(reader: StreamReader, writer: StreamWriter, timeout=30):
    async def session():
        try:
            async with async_timeout.timeout(timeout):
                with closing(writer):
                    data = await reader.readuntil(b'\r\n\r\n')
                    addr = writer.get_extra_info('peername')

                    print(f"Received {data} from {addr!r}")
                    request = RawHTTPParser(data)
                    print(f'Request: {str(request)}')

                    # if request.is_parse_error or request.check_user_agent:
                    #     print('HERE')
                    #     writer.write(b'HTTP/1.1 666 Error detected\r\n\r\n')
                    #     await writer.drain()
                    # elif request.method:  # https
                    await https_handler(reader, writer, data)
        except asyncio.TimeoutError:
            print('Timeout')

        print('Closed connection')

    asyncio.create_task(session())


async def sub_handler(reader: StreamReader, writer: StreamWriter, timeout=30):
    async def session():
        try:
            async with async_timeout.timeout(timeout):
                with closing(writer):
                    writer.write(b'HTTP/1.1 200 I am happy to see you again\r\n\r\n')
        except asyncio.TimeoutError:
            print('Timeout')
        print('Closed connection')

    asyncio.create_task(session())
