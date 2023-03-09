import asyncio

from handler import main_handler, sub_handler


async def create_server_tasks(loop):
    host = '0.0.0.0'
    ports = [(80, main_handler), (8000, sub_handler)]
    for port, handler in ports:
        print('Serving on {}'.format((host, port)))
        loop.create_task(asyncio.start_server(handler, host, port))


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(create_server_tasks(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    main()
