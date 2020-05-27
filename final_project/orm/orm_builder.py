from faker import Faker

from orm.model import Base, TestUsers
from orm.orm_client import MysqlOrmConnection

fake = Faker(locale='ru_RU')


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.create_table()

    def create_table(self):
        if not self.engine.dialect.has_table(self.engine, 'test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def del_user(self, username):
        return self.connection.session.query(TestUsers).filter(TestUsers.username == username).delete()

    def get_access(self, username):
        result = self.connection.session.query(TestUsers.access).filter(TestUsers.username == username).first()
        return None if len(result) != 1 else result[0]
