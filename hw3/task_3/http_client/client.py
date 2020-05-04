import socket
import json


class HTTP_Client:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def get(self, params):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((self.host, self.port))
        request = f'GET {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        client.send(request.encode())
        total_data = []
        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break

        data = ''.join(total_data).splitlines()
        result = {'status_code': data[0].split()[1]}
        for i in range(1, len(data)):
            if data[i] == '':
                break
            key, value = data[i].split(':', 1)
            result[key] = value
        result['content'] = '\n'.join(data[i + 1:])
        return json.dumps(result)

    def post(self, params, data):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((self.host, self.port))
        request = f'POST {params} HTTP/1.1\r\nHost:{self.host}\r\nContent-Type: application/x-www-form-urlencoded\r\n' \
                  f'Content-Length: {len(data)}\r\n\r\n{data}'
        client.send(request.encode())
        total_data = []
        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break

        data = ''.join(total_data).splitlines()
        result = {'status_code': data[0].split()[1]}
        for i in range(1, len(data)):
            if data[i] == '':
                break
            key, value = data[i].split(':', 1)
            result[key] = value
        result['content'] = '\n'.join(data[i + 1:])
        return json.dumps(result)
