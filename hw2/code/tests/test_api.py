import pytest

from api.mytarget_client import MyTargetClient


class TestApi:
    @pytest.fixture(scope='function')
    def api_client(self):
        email = 'test.qa20@yandex.ru'
        password = 'QWer1@'
        return MyTargetClient(email, password)

    @pytest.mark.API
    def test_create_segment(self, api_client):
        assert api_client.create_segment('renata1234567').status_code == 200

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        content = api_client.create_segment('renata1234567').json()
        assert api_client.delete_segment(content['id']).status_code == 204

