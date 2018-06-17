import sys

from abc import ABC, abstractmethod
import datetime
from autotrading.logger import get_logger
print(sys.path)
logger = get_logger("base_strategy")

class Strategy(ABC):

    @abstractmethod
    def run(self):
        pass

    def update_trade_status(self, db_handler=None, item_id=None, value=None):
        """

        :param db_handler(obj): 대상 데이터베이스의 모듈 객체
        :param item_id(dict): 업데이트조건
        :param value(dict): 업데이트하려는 문서의 컬럼과 값
        :return:
        """
        pass
        if db_handler is None or item_id is None or value is None:
            raise Exception("Need to buy value or status")
        db_handler.set_db_collection("trader","trade_status")
        db_handler.update_items(item_id,{"$set":value})

    def order_buy_transaction(self, machine=None, db_handler=None, currency_type=None, item=None, order_type="limit"):
        """
        
        :param machine(obj): 매수주문하려는 거래소 모듈 객체
        :param db_handler(obj): 매수주문 정보를 입력할 데이터베이스 모듈 객체 
        :param currency_type(str): 매수주문하려는 화폐 종류
        :param itemm(dict) : buy(매수하려는 화폐의 원화가격), buy_amount(매수하려는 화폐 가격), desired_value(매도할 원화 가격)
        :param order_type(str):
        :return:
            OrderId(str) :매수 주문 완료 후의 주문 Id
        """
        pass

        if currency_type is None or item is None:
            raise Exception("Need to param")
        
        # trader db로 이동후 trade_status 콜렉션으로 바꾼다
        db_handler.set_db_collection("trader","trade_status")
        result = machine.buy_order(currency_type= currency_type, price=str(item['buy']), qty=str(item["buy_amount"]),
                                    order_type= order_type)

        if result['status'] == "success":
            db_handler.insert_item({
                "status" : "BUY_ORDERED",
                "currency" : "currency_type",
                "buy_order_id": str(result["orderId"]),
                "buy_amount": float(item["buy_amount"]),
                "buy" : int(item["buy"]),
                "buy_order_time" : int(datetime.datetime.now().timestamp()),
                "desired_value" : int(item["desired_value"]),
                "machine" : str(machine)
            })
            return result["orderId"]
        else:
            logger.info(result)
            logger.info(item)
            db_handler.update_item({"_id":item["_id"]},{"error": "failed"})
            return None

    def order_sell_transaction(self, machine=None, db_handler=None, currency_type=None, item=None, order_type="limit"):
        """

        :param machine(obj): 매수주문하려는 거래소 모듈 객체
        :param db_handler(obj): 매수주문 정보를 입력할 데이터베이스 모듈 객체
        :param currency_type(str): 매수주문하려는 화폐 종류
        :param itemm(dict) : buy(매수하려는 화폐의 원화가격), buy_amount(매수하려는 화폐 가격), desired_value(매도할 원화 가격)
        :param order_type(str):
        :return:
            OrderId(str) :매수 주문 완료 후의 주문 Id
        """
        pass
        if currency_type is None or item is None:
            raise Exception("Need to param")
        db_handler.set_db_collection("trader","trade_status")
        result = machine.sell_order(currency_type=currency_type,
                                    price=str(item["desired_value"]),
                                    qty=str(round(item["real_buy_amount"],8)),
                                    order_type=order_type)

        if result["status"] == "success":
            sell_query_header = {
                "_id":item["_id"]
            }
            sell_query_detail={
                "$set":
                    {"status" : "SELL_ORDERED",
                     "desired_value": int(item["desired_value"]),
                     "sell_order_id" : str(result["orderId"]),
                     "error":"success"}
            }
            db_handler.update_item(sell_query_header,sell_query_detail)
        else:
            logger.info(result)
            logger.info(item)
            db_handler.update_item({"_id":item["_id"]},{"error":"failed"})
            return None

        pass

    def order_cancel_transaction(self, machine=None, db_handler=None, currency_type=None, item=None):
        """
        :param machine(obj): 취소주문하려는 거래소 모듈 객체
        :param db_handler(obj): 취소주문 정보를 입력할 데이터베이스 모듈 객체
        :param currency_type(str): 취소주문하려는 화폐 종류
        :param itemm(dict) : buy(매수하려는 화폐의 원화가격), buy_amount(매수하려는 화폐 가격), desired_value(매도할 원화 가격)
        :param order_type(str):
        :return:
            OrderId(str) :매수 주문 완료 후의 주문 Id
        """
        if currency_type is None or item is None:
            raise Exception("Need to param")

        db_handler.set_db_collection("trader","trade_status")
        if item["status"] == "BUY_ORDERED":
            result = machine.cancel_order(currency_type=currency_type,order_id=item["buy_order_id"])
            if result[0]["status"] =="success":
                sell_query_header = {
                    "_id": item["_id"]
                }
                sell_query_detail = {
                    "$set":
                        {"status": "CANCEL_ORDERED",
                         "cancel_order_time" : int(datetime.datetime.now().timestamp()),
                         "error": "success"}
                }
                db_handler.update_item(sell_query_header,sell_query_detail)
                return item["buy_order_id"]

            else:
                logger.info(result)
                logger.info(item)
                return None
        elif item["status"] == "SELL_ORDERED":
            result = machine.cancel_order(currency_type=currency_type, order_id=item["sell_order_id"])
            if result[0]["status"] =="success":
                sell_query_header = {
                    "_id": item["_id"]
                }
                sell_query_detail = {
                    "$set":
                        {"status": "CANCEL_ORDERED",
                         "cancel_order_time" : int(datetime.datetime.now().timestamp()),
                         "error": "success"}
                }
                db_handler.update_item(sell_query_header,sell_query_detail)
                return item["sell_order_id"]

            else:
                logger.info(result)
                logger.info(item)
                return None



