from client import MysqlConnection

db = MysqlConnection(user='root', password='123456', db_name='logs', delete=True)

TABLE_1 = '''
CREATE TABLE Total_Requests (
    count INTEGER PRIMARY KEY
)
'''

TABLE_2 = '''
CREATE TABLE Request_Methods (
    http_type VARCHAR(10) PRIMARY KEY,
    count INTEGER
    
)
'''

TABLE_3 = '''
CREATE TABLE Lagest_Requests (
    request_size INTEGER,
    url VARCHAR(50),
    request_code INTEGER
)
'''

TABLE_4 = '''
CREATE TABLE Client_Errors (
    IP VARCHAR(15),
    url VARCHAR(50),
    request_code INTEGER
)
'''

TABLE_5 = '''
CREATE TABLE Redirect_Requests (
    IP VARCHAR(15),
    url VARCHAR(50),
    request_code INTEGER
)
'''

db.execute_query(TABLE_1)
db.execute_query(TABLE_2)
db.execute_query(TABLE_3)
db.execute_query(TABLE_4)
db.execute_query(TABLE_5)
