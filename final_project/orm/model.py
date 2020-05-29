from sqlalchemy import Column, Integer, Index, SMALLINT, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TestUsers(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(16), default=None, unique=True, index=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    access = Column(SMALLINT, default=None)
    active = Column(SMALLINT, default=None)
    start_active_time = Column(DATETIME, default=None)

