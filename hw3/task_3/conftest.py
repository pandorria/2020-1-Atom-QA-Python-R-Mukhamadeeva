import pytest
from task_3.http_client import client

from task_3.mock import server as mock


@pytest.fixture(scope='session')
def mock_server():
    server = mock.run_mock()
    server_host = server._kwargs['host']
    server_port = server._kwargs['port']

    yield server_host, server_port

    session = client.HTTP_Client(server_host, server_port)
    session.get('/shutdown')
