import socket
import time


class Client:

    def __init__(self, host, pr, timeout=None):
        self.host = host
        self.pr = pr
        try:
            self.connection = socket.create_connection((self.host, self.pr), timeout)
        except socket.error as err:
            raise ClientError("error create connection", err)

    def _read(self):
        data = b""
        while not data.endswith(b"\n\n"):
            data += self.connection.recv(8196)
        dec_data = data.decode()
        status, answer = dec_data.split("\n", 1)
        answer = answer.strip()
        if status == "error":
            raise ClientError(answer)
        return answer

    def put(self, metric, metric_value, timestamp=None):
        timestamp = timestamp or str(int(time.time()))
        message = f"put {metric} {metric_value} {timestamp}\n".encode()
        self.connection.sendall(message)
        self._read()

    def get(self, metric):
        metric_dict = {}
        try:
            message = f"get {metric}\n".encode()
            self.connection.sendall(message)
        except socket.error as err:
            raise ClientError("error send message", err)
        answer = self._read()
        if answer == "":
            return metric_dict
        for note in answer.split('\n'):
            key, value, timestamp = note.split()
            if key not in metric_dict:
                metric_dict[key] = []
            metric_dict[key].append((int(timestamp), float(value)))
#        for key in metric_dict.keys():
#            metric_dict[key] = metric_dict[key].sort(it=lambda tup: tup[0])
        return metric_dict


class ClientError(Exception):
    pass


class ClientSocketError(Exception):
    pass


class ClientProtocolError(Exception):
    pass
