import unittest,inspect
from autotrading.db.mongodb.mongodb_handler import MongoDBHandler




class MongdoDBHandlerTestCase(unittest.TestCase):

    def SetUp(self):

        self.mongodb = MongoDBHandler("local", "coiner", "price_info")

        self.mongodb.delete_items({})
        docs = [
            {"currency" : "btc", "price":10000},
            {"currency" : "btc", "price":1000},
            {"currency" : "xrp", "price":100},
            {"currency" : "btc", "price":20000},
            {"currency" : "eth", "price":2000},
            {"currency" : "xrp", "price":200},
        ]

        self.mongodb.insert_items(docs)

    def test_set_db_collection(self):
        print('test_set_db_collection : ',inspect.stack()[0][3])

        self.mongodb.set_db_collection("trader","trade_status")
        self.assertEquals(self.mongodb.get_current_db_name(),"trader")
        self.assertEquals(self.mongodb.get_current_collection_name(),"trader")



    def test_get_collection(self):
        print(inspect.stack()[0][3])
        collection_name = self.mongodb.get_current_collection_name()
        self.assertEqual(collection_name, "price_info")

    def test_get_db_name(self):
        print(inspect.stack()[0][3])
        dbname = self.mongodb.get_current_db_name()
        self.assertEqual(dbname, "coiner")


    def test_insert_item(self):

        print(inspect.stack()[0][3])
        doc = {"item" : "item0" , "name" : "test_insert_item"}
        id = self.mongodb.insert_item(doc)
        assert id
        print(id)

    def test_insert_items(self):

        print(inspect.stack()[0][3])
        docs = [{"item" : "item1", "name" : "test_insert_items"},
               {"item": "item2", "name": "test_insert_items"}
               ]
        ids = self.mongodb.insert_items(docs)
        assert ids
        print(ids)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()



