import unittest
from autotrading.machine.bithumb_machine import BithumbMachine
import inspect


class BithumbMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.bithumb_machine = BithumbMachine()

    def test_get_ticker(self):

        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_ticker("ADA")
        assert ticker
        print(ticker)

    def test_get_filled_orders(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_filled_orders("ADA")
        assert ticker
        print(ticker)

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_wallet_status("ADA")
        assert ticker
        print(ticker)

    def test_get_my_order_status(self):
        print(inspect.stack()[0][3])
        result = self.bithumb_machine.get_my_order_status("ADA")
        assert result
        print(result)

    def test_buy_orders(self):
        print(inspect.stack()[0][3])
        result = self.bithumb_machine.buy_order("ADA",1,7000000)
        assert result
        print(result)

    def test_sell_order(self):
        print(inspect.stack()[0][3])
        result = self.bithumb_machine.sell_order("ADA", 340, 16)
        assert result
        print(result)

    def test_cancel_order(self):
        print(inspect.stack()[0][3])
        result = self.bithumb_machine.cancel_order("ADA", "ask", "1530534971444576")
        assert result
        print(result)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()