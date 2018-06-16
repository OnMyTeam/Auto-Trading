import requests,sys,os
import time
import math
from autotrading.machine.base_machine import Machine
import configparser
import json
import base64
import hashlib
import hmac
import urllib

# cur_dir = os.path.abspath(os.curdir)
# sys.path.append(cur_dir)
# PROJECT_HOME = cur_dir
# print(PROJECT_HOME)
# print(sys.path)
# nameconfig = os.path.abspath('config.ini')
# print(nameconfig)

class BithumbMachine(Machine):
    BASE_API_URL = "https://api.bithumb.com"
    TRADE_CURRENCY_TYPE = ["BTC","ETH","DASH","LTC","ETC","XRP","BCH","XMR","ZEC","QTUM","BTG","EOS",
                           "ICX", "VEN", "TRX", "ELF", "MITH", "MCO", "OMG", "KNC", "GNT", "HSR", "ZIL", "ETHOS","ALL"]

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('F:\\BitCoinDev\\conf\\config.ini')
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
        orders_api_path = "/public/transaction_history/{currency}".format(currency=currency_type)
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path, params)
        result = res.json()

        return result

    def microtime(self, get_as_float= False):
        if get_as_float:
            return time.time()

        else:
            return '%f %d' % math.modf(time.time())

    def usecTime(self):

        mt = self.microtime(False)

        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]

    def get_nonce(self):

        return self.usecTime()

    def get_signature(self, encoded_payload, secret_key):
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)
        api_sign = base64.b64encode(signature.hexdigest().encode('utf-8'))
        return api_sign

    def get_wallet_status(self,currency_type="BTC"):

        if currency_type is None:
            raise Exception("Need to currency_type")

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
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')
        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')
        h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512)
        hex_output = h.hexdigest();
        utf8_hex_output = hex_output.encode('utf-8')

        api_sign = base64.b64encode(utf8_hex_output)
        utf8_api_sign = api_sign.decode('utf-8')

        # curl_handle = pycurl.Curl()
        # curl_handle.setopt(pycurl.POST, 1)
        # # curl_handle.setopt(pycurl.VERBOSE, 1); # vervose mode :: 1 => True, 0 => False
        # curl_handle.setopt(pycurl.POSTFIELDS, str_data)
        #
        # url = self.BASE_API_URL + endpoint
        # curl_handle.setopt(curl_handle.URL, url)
        # curl_handle.setopt(curl_handle.HTTPHEADER,
        #                    ['Api-Key: ' + self.CLIENT_ID, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce])
        # # curl_handle.setopt(curl_handle.WRITEFUNCTION, self.body_callback)
        # curl_handle.perform()
        #
        # # response_code = curl_handle.getinfo(pycurl.RESPONSE_CODE); # Get http response status code.
        #
        # curl_handle.close()

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}

        res = requests.post(url_path, headers=headers, data=str_data)
        result = res.json()
        return result

    def get_list_my_orders(self, currency_type):
        """
        사용자의 현재 예약 중인 주문 현황을 조회하는 메서드 입니다.
        :param currency_type: 코인 이름
        :return:
            거래 중인 현황을 리스트로 반환합니다.
        """

        if currency_type is None:
            raise Exception("Need to currency_type")

        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception("Not Support currency type")
        time.sleep(1)
        endpoint ="/info/orders"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array = {
            "endpoint" : endpoint,
            "currency" : currency_type
        }

        uri_array = dict(endpoint_item_array)
        str_data = urllib.parse.urlencode(uri_array)
        nonce = self.get_nonce()
        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.CLIENT_SECRET
        utf8_key = key.encode('utf-8')
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Api-Key': self.CLIENT_ID,
                   'Api-Sign': self.get_signature(utf8_data, bytes(utf8_key)),
                   'Api-Nonce': nonce}
        res = requests.post(url_path,headers=headers, data=str_data)
        result = res.json()

        return result