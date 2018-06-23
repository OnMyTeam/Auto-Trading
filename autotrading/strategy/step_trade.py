import sys
from autotrading.strategy.base_strategy import Strategy
from autotrading.machine.bithumb_machine import BithumbMachine
from autotrading.db.mongodb.mongodb_handler import MongoDBHandler
from autotrading.pusher.slack import PushSlack
from autotrading.logger import get_logger

logger = get_logger("step_trade")

class StepTrade(Strategy):

    def __init__(self,machine=None, db_handler=None, strategy=None, currency_type=None, pusher=None):
        if machine is None or db_handler is None or currency_type is None or strategy is None:
            raise Exception("Need to machine, db, currency_type, Strategy")
        # isinstance(object, classinfo)
        # -> isinstance는 object가 classinfo의 인스턴스 인지 점검 후 True/False 값을 리턴한다.
        # -> isinstance를 이용하여 object의 데이터 타입을 확인 할 수 있다.
        if isinstance(machine,BithumbMachine):
            self.currency_type = currency_type

        self.machine = machine
        self.pusher = pusher
        result = self.db_handler.find_item({"name":"strategy"},"trader","trade_strategy")
        self.params = result[0]
        if self.params["is_active"]=="inactive":
            logger.info("inactive")
            return
        logger.info(self.currency_type)
        resultlast = self.machine.get_ticker(self.currency_type)
        self.last_val = int(resultlast["last"])

    def run(self):
        if self.params["is_activate"]=="active":
            self.check_my_order()
            self.scenario()

    def check_my_ordered(self):
        #Check by ordered

if __name__ == "__main__":
    mongodb = MongoDBHandler()
    bithumb_machine = BithumbMachine()
    pusher = PushSlack()

    if len(sys.argv) > 0:
        trader = StepTrade(machine=bithumb_machine, db_handler=mongodb, strategy=sys.argv[1], currency_type=sys.argv[2],
                           pusher=pusher)
        trader.run()



