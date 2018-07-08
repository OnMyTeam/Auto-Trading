from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser
from autotrading.db.base_handler import DBHandler



class MongoDBHandler(DBHandler):
    """
    PyMongo를 래핑해서 사용하는 클래스입니다. DBHandler 추상 클래스를 상속합니다.
    리모트 DB와 로컬 DB를 모두 사용할 수 있도록 __init__ 에서 mode로 구분합니다.

    """
    def __init__(self, mode="local", db_name=None, collection_name=None):
        """
        MongoDBHandler __init__ 구현부 .

        Args:
            mode (str): local DB인지 remote DB인지 구분합니다. ex) local, remote
            db_name (str): MongoDB에서 database에 해당하는 이름을 받습니다.
            collection_name (str): database에 속하는 collection 이름을 받습니다.

        Returns:
            None

        Raises:
            db_name과 collection_name이 없으면 Exception을 발생시킵니다.
        """
        if db_name is None or collection_name is None:
            raise Exception("Need to db name and collection name")
        config = configparser.ConfigParser()
        config.read('F:/BitCoinDev/BitCoinDev_Pycharm/conf/config.ini')

        self.db_config = {}
        self.db_config["local_ip"] = config['MONGODB']['local_ip']
        self.db_config["port"] = config['MONGODB']['port']
        self.db_config["remote_host"] = config['MONGODB']['remote_host']
        # self.db_config["remote_port"] = config['MONGODB']['remote_port']
        self.db_config["user"] = config['MONGODB']['user']
        self.db_config["password"] = config['MONGODB']['password']

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))

        if mode == "local":
            self._client = MongoClient("mongodb://{local_ip}:{port}".format(**self.db_config))


        self._db = self._client[db_name]

        self._collection = self._db[collection_name]



    def set_db_collection(self, db_name=None, collection_name=None):
        """
        MongoDB에서 작엽하려는 데이터베이스와 콜렉션을 변경할 때 사용한다.

         db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받는다.
         collection: 데이터베이스에 속하는 콜렉션 이름을 받습니다.

        """

        if db_name is None:
            raise Exception("Need to dbname name")

        self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db_name(self):

        return self._db.name

    def get_current_collection_name(self):

        return self._collection.name


    def insert_item(self, data, db_name=None, collection_name=None):
        if db_name is not None:
            self._db = self._client[db_name]

        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.insert_one(data).inserted_id

    def insert_items(self, datas, db_name=None, collection_name=None):
        if db_name is not None:
            self._db = self._client[db_name]

        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.insert_many(datas).inserted_ids

    def find_item(self, condition=None, db_name=None, collection_name=None):

        if condition is None:
            condition ={}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.find_one(condition)

    def find_items(self, condition=None, db_name=None, collection_name=None):

        if condition is None:
            condition ={}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)

    def update_items(self,condition=None, update_value=None, db_name=None, collection_name=None):
        if condition is None:
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.update_many(filter=condition, update=update_value)

    def aggregate(self,pipline=None, db_name=None, collection_name=None):

        if pipline is None:
            raise Exception("Need to Pipline")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.aggregate(pipline)


    def delete_items(self,condition=None, db=None, collection=None):

        if condition is None:
            raise Exception("Need to condition")
        if db is not None:
            self._db = self._client[db]
        if collection is not None:
            self._collection = self._db[collection]
        return self._collection.delete_many(condition)


    def test(self,type,doc,update_value=None):
        if type=="insert_items":

            aaa.insert_items(doc)

        if type=="insert_item":

            aaa.insert_item(doc)
        if type=="delete_items":
            aaa.delete_items({})

        if type=="find_item":
            doc = aaa.find_item(doc)
            print(doc)
        if type=="find_items":
            doc = aaa.find_items(doc)
            for i in doc:
                print(i)
        if type=="update_items":
            aaa.update_items(doc,update_value)

if __name__ == "__main__":

    aaa = MongoDBHandler("local", "coiner", "price_info")
    docs = [
        {"$match":{"currency":"btc"}},
        {"$group":{"_id" : "$currency",
                   "min_val": {"$min":"$price"},
                   "max_val": {"$max":"$price"},
                   "sum_val": {"$sum":"$price"}
                    }
         }
    ]
    result = aaa.aggregate(docs)
    assert result
    for i in result:
        print(i)