from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser
from autotrading.db.base_handler import DBHandler



class MongoDBHandler(DBHandler):
    """
    PyMongo를 래핑해서 사용하는 클래스입니다. DBHandler 추상 클래스를 상속합니다.
    리모트 DB와 로컬 DB를 모두 사용할 수 있도록 __init__ 에서 mode로 구분합니다.

    """
    def __init__(self,mode="local",db_name=None,collection_name=None):

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))

        elif mode =="local":
            self._client = MongoClient("mongodb://{user}:{password}@{local_ip}:{port}".format(**self.db_config))
            print(self._client)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]


