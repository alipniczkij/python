import asyncio

storage = []


class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        method, metric = data.decode()[:-1].split(' ', 1)
        if method == "put":
            resp = self._put(metric)
        elif method == "get":
            resp = self._get(metric)
        else:
            resp = "error\nwrong command\n\n"
        self.transport.write(resp.encode())

    @staticmethod
    def _put(data):
        if len(data) != 3:
            return "error\nwrong command\n\n"
        check = list(filter(lambda chk: chk == data, storage))
        if len(check) == 0:
            storage.append(data)
        return "ok\n\n"

    @staticmethod
    def _get(data):
        if len(data) != 1:
            return "error\nwrong command\n\n"
        answer = ''
        for i in range(len(storage)):
            if data == "*":
                answer += '\n' + storage[i]
            else:
                if data in storage[i]:
                    answer += '\n' + storage[i]
        answer += '\n\n'
        return f"ok{answer}"


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    cor = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(cor)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()
