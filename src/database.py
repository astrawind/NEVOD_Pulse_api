from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import backoff

class DataBaseConnection(AbstractContextManager):
    def __init__(self, ):
        self._connection = None

    def __enter__(self):
        self.connect()
        return self
    
    @abstractmethod
    def _get_connection(): ...

    @abstractmethod
    def _delete_connection(): ...

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    def connect(self):
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection

    def disconnect(self):
        if self._connection is not None:
            self._delete_connection(self._connection)
            self._connection = None

class PostgresConnection(DataBaseConnection):
    def __init__(self, username, password, host, port, databasename):
        super().__init__(self)
        self.__url = f'postgresql://{username}:{password}@{host}:{port}/{databasename}'

    def _get_connection(self):
        engine = create_engine(self.__url)
        return Session(engine)
    
    def _delete_connection(self):
        self._connection.close()