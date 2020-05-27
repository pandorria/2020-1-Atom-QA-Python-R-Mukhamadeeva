import pytest
import allure

from api.api_client import ApiClient
from orm.orm_client import MysqlOrmConnection
from orm.orm_builder import MysqlOrmBuilder


class TestApi:
    @pytest.fixture(scope='function', autouse=True)
    def database(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    @pytest.fixture(scope='function')
    def api_client(self):
        username = 'rootuser'
        password = '12345'
        email = 'test@yandex.ru'
        return ApiClient(username, password, email)

    def test_add_user_correct(self, api_client):
        """
        Тестируется добавление пользователя с корректно заполненными полями. Пользователь успешно добавляется
        Ожидаемый статус код - 210. API отрабатывает корректно
        """
        username = 'qwertyrwerwe'
        result = api_client.reg_user(username, 'renata@yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 210

    def test_add_user_incorrect_username_length(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя с некорректной
        длиной поля "username"
        Ожидаемый статус код - 400 "Плохой запрос"
        АPI работает некорректно: пользователь с таким username добавляется в базу и возвращается статус-код 210
        """
        username = 'q'
        result = api_client.reg_user(username, 'qqqqqqqq@yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 400

    def test_add_user_russian_username(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя с русским значением "username"
        Ожидаемый статус код - 400 "Плохой запрос"
        АPI работает некорректно: пользователь с таким username добавляется в базу и возвращается статус-код 210
        """
        username = 'Мирослава'
        result = api_client.reg_user(username, 'miroslava@yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 400

    def test_add_user_invalid_email(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя сo значением "email",
        не проходящим под стандартную маску почты
        Ожидаемый статус код - 400 "Плохой запрос"
        АPI работает некорректно: пользователь с таким email добавляется в базу и возвращается статус-код 210
        """
        username = 'cvbinokil'
        result = api_client.reg_user(username, 'yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 400

    def test_add_user_russian_email(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя с русским значением "email"

        Ожидаемый статус код - 400 "Плохой запрос"
        АPI работает некорректно: пользователь с таким email добавляется в базу и возвращается статус-код 210

        Данный тест необходим, так как тестировщику неизвестно, под каким регулярным выражением производится валидация,
        и в результате тест показал, что разработка не учла возможность ввода русских букв в адрес эл.почты
        """
        username = 'qwertyuio'
        result = api_client.reg_user(username, 'текстнарусском', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 400

    def test_add_user_exist_email(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя с существующим в базе email.
        Тест представляет собой 2 POST запроса с идентичными значениями email

        Ожидаемый статус код - 304 "Сущность существует/не изменилась"
        АPI работает некорректно: возвращается статус-код 210, а пользователь не заносится в базу
        """
        username = '123456'
        api_client.reg_user(username, 'useremail@yandex.ru', 'rwrwerwerwr')
        result = api_client.reg_user('654321', 'useremail@yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 304

    def test_add_user_exist_username(self, api_client):
        """
        Тестируется негативный сценарий, когда производится попытка добавить пользователя с существующим в базе username
        Тест представляет собой 2 POST запроса с идентичными значениями username

        Ожидаемый статус код - 304 "Сущность существует/не изменилась"
        АPI работает некорректно: возвращается статус-код 210, а пользователь не заносится в базу
        """
        username = 'ooooooooo'
        api_client.reg_user(username, 'useremail1@yandex.ru', 'rwrwerwerwr')
        result = api_client.reg_user(username, 'useremail2@yandex.ru', 'rwrwerwerwr')
        self.builder.del_user(username)
        assert result == 304

    def test_del_user(self, api_client):
        """
        Тестируется удаление пользователя из базы. Тет представляет собой get запрос на удаление ранее созданного
        пользователя

        Ожидаемый статус код - 204 "Сущность удалена".
        API отрабатывает корректно
        """
        username = 'fffffff'
        api_client.reg_user(username, 'fffffff@yandex.ru', 'rwrwerwerwr')
        result = api_client.del_user(username)
        self.builder.del_user(username)
        assert result == 204

    def test_del_not_exist_user(self, api_client):
        """
        Тестируется негативный сценарий на удаление несуществующего пользователя из базы.
        Теcт представляет собой get запрос на удаление не созданного ранее пользователя

        Ожидаемый статус код - 404 "Сущности не существует".
        API отрабатывает корректно
        """
        assert api_client.del_user('unreal_user') == 404

    def test_block_user(self, api_client):
        """
        Тестируется блокировка пользователя, существующего в базе.
        Добавляется пользователь, флаг active изначально выставлен 1.
        После выполнения GET запроса на блокировку флаг меняется на 0.

        Ожидаемый статус код - 200 "Действие выполнено"
        API отрабатывает корректно
        """
        username = 'ssssssss'
        api_client.reg_user(username, 'ssssssss@yandex.ru', 'rwrwerwerwr')
        result_code = api_client.block_user(username)
        result_flag = self.builder.get_access(username)
        self.builder.del_user(username)
        assert result_code == 200
        assert result_flag == 0

    def test_block_not_exist_user(self, api_client):
        """
        Тестируется негативный сценарий на блокировку несуществующего в базе пользователя.
        Теcт представляет собой get запрос на блокировку не созданного ранее пользователя

        Ожидаемый статус код - 404 "Сущности не существует".
        API отрабатывает корректно
        """
        username = 'cvtybiuonijlkb'
        assert api_client.block_user(username) == 404

    def test_block_user_without_accept(self, api_client):
        """
        Тестируется негативный сценарий на блокировку уже заблокированного пользователя с флагом 0.
        Тест представляет собой POST запрос с созданием пользователя и 2 идентичных GET запроса на его блокировку

        Ожидаемый статус код - 304 "Сущность существует/не изменилась".
        API отрабатывает корректно

        """
        username = 'jjjjjjjj'
        api_client.reg_user(username, 'jjjjjjjj@yandex.ru', 'rwrwerwerwr')
        api_client.block_user(username)
        result = api_client.block_user(username)
        self.builder.del_user(username)
        assert result == 304

    def test_accept_user(self, api_client):
        """
        Тестируется разблокировка пользователя, существующего в базе.
        В рамках теста в базу добавляется пользователь, выполняется GET запрос на блокировку данного пользователя,
        флаг active выставляется в 0. После этого выполняется GET запрос на разблокировку, флан active становится 1

        Ожидаемый статус код - 200 "Действие выполнено"
        API отрабатывает корректно
        """
        username = 'wwwwwwww'
        api_client.reg_user(username, 'wwwwwww@yandex.ru', 'rwrwerwerwr')
        api_client.block_user(username)
        result_code = api_client.accept_user(username)
        result_flag = self.builder.get_access(username)
        self.builder.del_user(username)
        assert result_code == 200
        assert result_flag == 1

    def test_accept_user_with_accept(self, api_client):
        """
        Тестируется негативный сценарий на разблокировку пользователя с флагом active 1.
        Теcт представляет собой get запрос на разблокировку пользователя, имеющего в данный момент доступ
        Ожидаемый статус код - 304 "Сущность существует/не изменилась".
        API отрабатывает корректно
        """
        username = 'ijnjijhb'
        api_client.reg_user(username, 'ijnjijhb@yandex.ru', 'rwrwerwerwr')
        result = api_client.accept_user(username)
        self.builder.del_user(username)
        assert result == 304

    def test_accept_not_exist_user(self, api_client):
        """
        Тестируется негативный сценарий на разблокировку несуществующего в базе пользователя.

        Ожидаемый статус код - 404 "Сущности не существует". API отрабатывает корректно
        """
        username = 'asdfghk'
        assert api_client.accept_user(username) == 404
