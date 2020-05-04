import pytest
import json
from task_3.http_client import client
from task_3.mock import server


def add_user(user_id: int, user_data: dict):
    server.users.update({str(user_id): user_data})


class TestMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mock_server):
        self.server_host, self.server_port = mock_server
        self.client = client.HTTP_Client(self.server_host, self.server_port)
        user = {'name': 'TEST_1'}
        add_user(1, user)
        user = {'name': 'TEST_2'}
        add_user(2, user)

    def test_get_correct(self):
        result = self.client.get('/get_user/1')
        content = json.loads(result)
        assert int(content['status_code']) == 200 and content['content'] == 'TEST_1'

    def test_get_invalid(self):
        result = self.client.get('/get_user/3')
        content = json.loads(result)
        assert int(content['status_code']) == 404

    def test_post_invalid(self):
        result = self.client.post('/add_user', 'test')
        content = json.loads(result)
        assert int(content['status_code']) == 400

    def test_post_correct(self):
        result = self.client.post('/add_user', 'id=3&name=renata')
        content = json.loads(result)
        assert int(content['status_code']) == 200
