import requests
import time
import math
from autotrading.machine.base_machine import Machine
import configparser
import json
import base64
import hashlib
import hmac
import urllib

class BithumbMachine(Machine):
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC","ETH","DASH","LTC","ETC","XRP","BCH","XMR","ZEC","QTUM","BTG","EOS",
                           "ICX", "VEN", "TRX", "ELF", "MITH", "MCO", "OMG", "KNC", "GNT", "HSR", "ZIL", "ETHOS","ALL"]

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('../conf/config.ini')
        self.CLIENT_ID = config['Bithumb']['connect_key']
        self.CLIENT_SECRET = config['Bithumb']['secret_key']

        # self.USER_NAME = config['Bithumb']['username']

    def get_ticker(self,currency_type=None):
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support current type')
        time.sleep(1)

        ticker_api_path = "/public/ticker/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path)
        response_json = res.json()

        result = {}

        result["timestamp"] = str(response_json['data']["date"])
        result["last"] = str(response_json['data']["closing_price"])
        result["bid"] = str(response_json['data']["buy_price"])
        result["ask"] = str(response_json['data']["sell_price"])
        result["high"] = str(response_json['data']["max_price"])
        result["low"] = str(response_json['data']["min_price"])
        result["volume"] = str(response_json['data']["volume_1day"])

        return result

