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

