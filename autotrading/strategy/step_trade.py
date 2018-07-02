import sys
import traceback

from autotrading.strategy.base_strategy import Strategy
from autotrading.machine.bithumb_machine import BithumbMachine
from autotrading.db.mongodb.mongodb_handler import MongoDBHandler
from autotrading.pusher.slack import PushSlack
from autotrading.logger import get_logger

logger = get_logger("step_trade")


class StepTrade(Strategy):

    def __init__(self, machine=None, db_handler=None, strategy=None, currency_type=None, pusher=None):
        if machine is None or db_handler is None or currency_type is None or strategy is None:
            raise Exception("Need to machine, db, currency_type, Strategy")
        # isinstance(object, classinfo)
        # -> isinstance는 object가 classinfo의 인스턴스 인지 점검 후 True/False 값을 리턴한다.
        # -> isinstance를 이용하여 object의 데이터 타입을 확인 할 수 있다.
        if isinstance(machine, BithumbMachine):
            self.currency_type = currency_type

        self.machine = machine
        self.pusher = pusher
        self.db_handler = db_handler
        result = self.db_handler.find_item({"name": "strategy"}, "trader", "trade_strategy")
        self.params = result[0]
        if self.params["is_active"] == "inactive":
            logger.info("inactive")
            return
        logger.info(self.currency_type)
        resultlast = self.machine.get_ticker(self.currency_type)
        self.last_val = int(resultlast["last"])

    def run(self):
        if self.params["is_activate"] == "active":
            self.check_my_order()
            self.scenario()

    def check_my_order(self):
        # Check by ordered
        self.check_buy_ordered()
        self.check_buy_completed()
        self.check_sell_ordered()
        self.check_sell_completed()
        self.check_keeep_ordered()

    # 지속해서 주문할 목록들을 체크해서 일괄적으로 매수 주문함
    def check_buy_ordered(self):
        condition = {"currency": self.currency_type, "status": "BUY_ORDERED"}
        buy_orders = self.db_handler.find_item(condition, "trader", "trade_status")
        for item in buy_orders:
            logger.info(item)
            order_result = self.machine.get_my_order_status(self.currency_type)
            logger.info(order_result)

            if len(order_result) > 0 and order_result["data"]["status"] != "placed" and order_result["data"]["price"]==item["buy"]:
                order_result_dict = order_result["data"]
                # 매수 체결되면 상태값 업데이트
                real_buy_amount = float(order_result_dict["units"]) - float(order_result_dict["fee"])
                real_buy_value = float(order_result_dict["units"]) - float(order_result_dict["fee"])
                completed_time = int(order_result_dict["date_completed"]/1000)
                fee = float(order_result_dict["fee"])

                if order_result_dict["type"] == "bid":
                    item_id = {"_id" : item["_id"]}
                    value = {"status":"BUY_COMPLETED",
                             "real_buy_amount" : real_buy_amount,
                             "buy_completed_time" : completed_time}
                    self.update_trade_status(db_handler=self.db_handler,item_id=item_id, value=value )
                    self.pusher.send_message(thread="#general", message= "buy_completed : %s" % (str(item)))
            elif len(order_result) > 0 and order_result["data"]["status"] == "placed" and order_result["data"]["price"] == str(item["buy"]):
                # 채결된 화폐의 마지막 거래금액이 주문한 화폐 가격과 step_value 금액보다 작으면 취소함
                if int(item["buy"]) + int(self.params["step_value"]) <= self.last_val:
                    logger.info("CancelOrder")
                    logger.info(item)
                    #Cancel Order
                    try:
                        self.order_cancel_transaction(machine=self.machine, db_handler=self.db_handler, currency_type=self.currency_type,
                                                  item=item)
                    except:
                        error = traceback.format_exc()
                        logger.info(error)
                        item_id = {"_id" : item["_id"]}
                        value = {"error": "failed"}
                        self.update_trade_status(db_handler=self.db_handler, item_id=item_id, value=value)
                        self.pusher.send_message("#general", "err cancel: %s" % (str(item)))
            elif len(order_result) == 0:
                item_id = {"_id": item["_id"]}
                value = {"status": "CANCEL_ORDERED"}
                self.update_trade_status(db_handler=self.db_handler, item_id=item_id, value=value)


    # 실제 매수 완료된 리스트를 불러와 매도 가능 상태로 만들어버림
    def check_buy_completed(self):
        query = {
            "currency" : self.currency_type,
            "status" : "BUY_COMPLETED"
        }
        buy_completed = self.db_handler.find_item(query, "trader", "trade_status")
        logger.info("BUY_COMPLETED")
        for item in buy_completed:
            logger.info(item)
            try:
                self.order_sell_transaction(machine=self.machine, db_handler=self.db_handler, currency_type=self.currency_type,
                                            item=item)
            except:
                error = traceback.format_exc()
                logger.info(error)
                self.update_trade_status(db_handler=self.db_handler, item_id={"_id":item["_id"]}, value={"error" : "failed"})

    #     매도 주문 때린 상태를 불러와 실제 매도가 됬는지 확인
    def check_sell_ordered(self):
        #check sell ordered
        query = {
            "currency" : self.currency_type,
            "status" : "SELL_ORDERED"
        }
        sell_orders = self.db_handler.find_item(query, "trader", "trade_status")
        for item in sell_orders:
            logger.info(item)
            if "sell_order_id" in item:
                order_result = self.machine.get_my_order_status(self.currency_type, item["sell_order_id"])
                if order_result is not None:
                    logger.info(order_result)
                else:
                    continue

            if len(order_result) > 0 and order_result["data"]["status"] != "placed" and order_result["data"]["price"] == str(item["desired_value"]):
                order_result_dict = order_result["data"]
                real_sell_amount = float(order_result_dict["units"])
                real_sell_value = float(order_result_dict["price"])
                completed_time = int(order_result_dict["date_completed"]/1000)
                fee = float(order_result_dict["fee"])
                if order_result_dict["type"] == "ask":
                    item_id = {"_id" : item["_id"]}
                    query = {
                        "status": "SELL_COMPLETED`",
                        "real_sell_amount": real_sell_amount,
                        "sell_completed_time": completed_time,
                        "real_sell_value": real_sell_value,
                        "sell_fee": fee
                    }
                    self.update_trade_status(db_handler= self.db_handler, item_id=item_id, value=query)
                    self.pusher.send_message("#general", "sell_completed: %s" % (str(item)))

            elif len(order_result) > 0 and order_result["data"]["status"] == "placed" and order_result["data"]["price"] == str(item["desired_value"]):
                if int(item["desired_value"]) > self.last_val * 1.15:
                    print(item)
                    self.order_cancel_transaction(machine=self.machine, db_handler=self.db_handler, currency_type=self.currency_type,
                                                  item=item)
                    item_id = {"_id" : item["_id"]}
                    query = {
                        "status": "KEEP_ORDERED",
                     }
                    self.update_trade_status(db_handler=self.db_handler, item_id=item_id, value=query)
                    #self.pusher.send_message("#general", "Keeped: %s" % (str(item)))

    def check_sell_completed(self):
        query = {
            "currency": self.currency_type,
            "$or": [{"status": "SELL_COMPLETED"}, {"status": "CANCEL_ORDERED"}]
        }
        sell_completed = self.db_handler.find_item(query, "trader", "trade_status")
        for item in sell_completed:
            self.db_handler.insert_item(item, "trader", "trade_history")
            self.db_handler.delete_item({"_id": item["_id"]}, "trader", "trade_status")

    def check_keep_ordered(self):
        keeped_orders = self.db_handler.find_item({"currency": self.currency_type,
                                                   "status": "KEEP_ORDERED"}, "trader", "trade_status")
        for item in keeped_orders:
            if int(item["desired_value"]) * 0.9 < self.last_val:
                self.order_buy_transaction(machine=self.machine, db_handler=self.db_handler, currency_type=self.currency_type,
                                           item=item)
                logger.info("sell order form keeped %s" % (str(item["_id"])))







if __name__ == "main":
    mongodb = MongoDBHandler()
    bithumb_machine = BithumbMachine()
    pusher = PushSlack()

    if len(sys.argv) > 0:
        trader = StepTrade(machine=bithumb_machine, db_handler=mongodb, strategy=sys.argv[1], currency_type=sys.argv[2],
                           pusher=pusher)
        trader.run()
