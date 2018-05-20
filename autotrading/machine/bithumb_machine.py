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

    def get_ticker(self,currency_type="BTC"):
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

    def get_filled_orders(self, currency_type="BTC"):

        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception("Not support currency Type")
        time.sleep(1)

        params = {'offfset':0,'count':100}
        orders_api_path = "/public/recent_transactions/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path,params)
        result = res.json()

        return result

    def microtime(self, get_as_float = False):
        if get_as_float:
            return time.time()

        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self):

        mt = self.microtime(False)
        print(mt)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]

    def get_nonce(self):
        print(self.usecTime())
        return self.usecTime()

    def get_signature(self, encoded_payload, secret_key):
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)
        api_sign = base64.b64encode(signature.hexdigest().encode('utf-8'))
        return api_sign

    def get_wallet_status(self,currency_type="BTC"):

        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not Support currency type')

        time.sleep(1)

        wallet_status_api_path = "/info/balance"
        endpoint = "/info/balance"

        url_path = self.BASE_API_URL + wallet_status_api_path

        endpoint_item_array = {
            "endpoint" : endpoint,
            "currency" : currency_type
        }

        uri_array = dict(endpoint_item_array)
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.usecTime()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result


