from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import logging
from .exceptions import DataBaseError

import backoff
from pymongo import MongoClient
from pymongo.errors import PyMongoError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

class DatabaseConnectionMaker(ABC):
    @abstractmethod
    def __call__(self):
        pass

class PostresConnectionMaker(DatabaseConnectionMaker):

    def __init__(self, username, password, host, port, databasename, pool_size=5):
        logger.debug('creating Postgres engine')
        self.engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{databasename}', pool_size=pool_size)
        self.maker = sessionmaker(self.engine, expire_on_commit=False)

    def __call__(self):
        try:
            return self.maker()
        except Exception as e:
            raise DataBaseError(str(e))
        
class MongoConnectionMaker(DatabaseConnectionMaker):
    def __init__(self, username, password, host, port, databasename, pool_size=100):
        self._client = MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/",
            maxPoolSize=pool_size
        )
        self._databasename = databasename
        
    def __call__(self):
        return self._client[self._databasename]