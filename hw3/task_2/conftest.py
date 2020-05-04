import pytest

from orm_client import MysqlOrmConnection


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('root', '123456', 'TEST_PYTHON_ORM')
