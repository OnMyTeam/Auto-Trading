import unittest
from autotrading.machine.bithumb_machine import BithumbMachine
import inspect


class BithumbMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.bithumb_machine = BithumbMachine()

    def test_get_ticker(self):

        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_ticker("TRX")
        assert ticker
        print(ticker)

    def test_get_filled_orders(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_filled_orders("LTC")
        assert ticker
        print(ticker)

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_wallet_status("BTC")
        assert ticker
        print(ticker)

    def test_get_list_my_orders(self):
        print(inspect.stack()[0][3])
        result = self.bithumb_machine.get_list_my_orders("BTC")
        assert result
        print(result)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()