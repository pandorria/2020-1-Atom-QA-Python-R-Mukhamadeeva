import pytest

from model import Prepod
from orm_client import MysqlOrmConnection
from orm_builder import MysqlOrmBuilder


class TestOrmMysql:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_create(self):
        assert self.builder.engine.dialect.has_table(self.builder.engine, 'prepods')
