from faker import Faker

from model import Base, Prepod
from orm_client import MysqlOrmConnection

fake = Faker(locale='ru_RU')


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.create_prepods()

    def create_prepods(self):
        if not self.engine.dialect.has_table(self.engine, 'prepods'):
            Base.metadata.tables['prepods'].create(self.engine)
