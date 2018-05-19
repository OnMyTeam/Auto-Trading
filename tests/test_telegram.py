import unittest
from autotrading.pusher.telegram import PushTelegram


class TestTelegram(unittest.TestCase):

    def setUp(self):
        self.pusher = PushTelegram()

    def test_send_message(self):
        self.pusher.send_message("@sangiki82", "<a href='http://www.naver.com'>aaa</a>")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()