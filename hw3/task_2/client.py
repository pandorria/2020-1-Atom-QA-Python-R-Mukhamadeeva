import pymysql


class MysqlConnection:
    def __init__(self, user, password, db_name, delete=False):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '127.0.0.1'
        self.port = 3306

        self.connection = self.connect(delete)

    def get_connection(self, db_created=False):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db_name if db_created else None,
            charset='utf8',
            autocommit=True,

        )

    def connect(self, delete):
        if delete:
            connection = self.get_connection()
            connection.query(f'DROP DATABASE if exists {self.db_name}')
            connection.query(f'CREATE DATABASE {self.db_name}')
            connection.close()

        return self.get_connection(db_created=True)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()

        return res
