import unittest
from autotrading.pusher.slack import PushSlack


class TestSlacker(unittest.TestCase):

    def setUp(self):
        self.pusher = PushSlack()

    def test_send_message(self):
        message = "<a href='http://www.naver.com'>aaaa</a>"
        self.pusher.send_message("#general", message)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()