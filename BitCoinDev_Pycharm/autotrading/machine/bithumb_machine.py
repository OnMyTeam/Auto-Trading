import requests,sys,os
import time
import math
from autotrading.machine.base_machine import Machine
from autotrading.machine.xcoin_api_client import *
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
    TRADE_CURRENCY_TYPE = ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM", "BTG", "EOS",
                           "ICX", "VEN", "TRX", "ELF", "MITH", "MCO", "OMG", "KNC", "GNT", "HSR", "ZIL", "ETHOS",
                           "PAY", "WAX", "POWR", "LRC", "GTO", "STEEM", "STRAT", "ZRX", "REP", "AE", "XEM", "SNT",
                           "ADA", "ALL"]
    # 'F:\\BitCoinDev\\conf\\config.ini
    def __init__(self):

        config = configparser.ConfigParser()
        config.read('F:/BitCoinDev/BitCoinDev_Pycharm/conf/config.ini')
        self.CLIENT_ID = config['Bithumb']['connect_key']
        self.CLIENT_SECRET = config['Bithumb']['secret_key']

        # self.USER_NAME = config['Bithumb']['username']

    def exception_Currency(self,currency_type):
        if currency_type is None:
            raise Exception("Need to currency_type")

        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception("Not Support currency type")

    def common_function(self, endpoint, endpoint_item_array):

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

        return str_data,headers

    def get_ticker(self, currency_type="BTC"):
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

    def get_wallet_status(self, currency_type="ADA"):

        if currency_type is None:
            raise Exception("Need to currency_type")

        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not Support currency type')

        time.sleep(1)

        wallet_status_api_path = "/info/balance"
        endpoint = "/info/balance"

        url_path = self.BASE_API_URL + wallet_status_api_path

        # endpoint_item_array = {
        #     "endpoint" : endpoint,
        #     "currency" : currency_type
        # }
        #
        # str_data, headers = self.common_function(endpoint,endpoint_item_array)
        rgParams = {
            "order_currency": currency_type,
            "payment_currency": "KRW"
        }
        api = XCoinAPI(self.CLIENT_ID,self.CLIENT_SECRET)
        response = api.xcoinApiCall(endpoint,rgParams)


        # res = requests.post(url_path, headers=headers, data=str_data)
        # result = res.json()
        return response

    def get_my_order_status(self, currency_type=None):
        """
        사용자의 현재 예약 중인 주문 현황을 조회하는 메서드 입니다.
        :type currency_type: object
        :param currency_type: 코인 이름
        :return:
            거래 중인 현황을 리스트로 반환합니다.
        """

        self.exception_Currency(currency_type)

        time.sleep(1)
        endpoint ="/info/orders"
        url_path = self.BASE_API_URL + endpoint

        # endpoint_item_array = {
        #     "endpoint" : endpoint,
        #     "currency" : currency_type
        # }
        #
        # str_data, headers = self.common_function(endpoint, endpoint_item_array)
        # res = requests.post(url_path,headers=headers, data=str_data)
        # result = res.json()
        rgParams = {
            "currency": currency_type,

        }
        api = XCoinAPI(self.CLIENT_ID,self.CLIENT_SECRET)
        response = api.xcoinApiCall(endpoint, rgParams)
        return response
    def buy_order(self, currency_type=None, price=None, qty=None, order_type="bid"):
        """
        매수주문 실행 매소드
        :param currency_type(str): 화폐종류 
        :param price(int): 1개 수량 주문에 해당하는 원화값 
        :param qty: 주문 수량
        :param order_type: 
        :return: 주문 상태 반환
        """
        self.exception_Currency(currency_type)
        time.sleep(1)
        endpoint = "/trade/place"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array ={
            "endpoint": endpoint,
            "order_currency": currency_type,
            "payment_currenct": "KRW",
            "units": qty,
            "price": price,
            "type": "bid"
        }
        str_data, headers = self.common_function(endpoint,endpoint_item_array)
        res = requests.post(url_path,headers=headers, data=str_data)
        result = res.json()

        return result

    def sell_order(self, currency_type=None, price=None, qty=None, order_type="ask"):
        """
        매도주문 실행 매소드
        :param currency_type(str): 화폐종류
        :param price(int): 1개 매도 주문에 해당하는 원화값
        :param qty: 매도 주문 수량
        :param order_type:
        :return: 매도 상태 반환
        """
        self.exception_Currency(currency_type)
        time.sleep(1)
        endpoint = "/trade/place"
        url_path = self.BASE_API_URL + endpoint

        endpoint_item_array ={
            "endpoint": endpoint,
            "order_currency": currency_type,
            "payment_currenct": "KRW",
            "units": qty,
            "price": price,
            "type": "ask"
        }
        str_data, headers = self.common_function(endpoint,endpoint_item_array)
        res = requests.post(url_path,headers=headers, data=str_data)
        result = res.json()

        return result

    def cancel_order(self, currency_type=None, order_type=None, order_id=None):
        """
        매수주문 실행 매소드
        :param currency_type(str): 화폐종류
        :param price(int): 1개 수량 주문에 해당하는 원화값
        :param qty: 주문 수량
        :param order_type(str): 취소하려는 주문이 종류(매수, 매도)
        :param order_id: 취소 주문하려는 주문의 ID
        :return: 주문 상태 반환
        """
        self.exception_Currency(currency_type)
        time.sleep(1)
        endpoint = "/trade/cancel"
        url_path = self.BASE_API_URL + endpoint

        # endpoint_item_array ={
        #     "endpoint": endpoint,
        #     "order_currency": currency_type,
        #     "type": order_type,
        #     "order_id": order_id
        # }
        # str_data, headers = self.common_function(endpoint,endpoint_item_array)
        # res = requests.post(url_path,headers=headers, data=str_data)
        # result = res.json()

        rgParams = {
            "currency": currency_type,
            "type": order_type,
            "order_id": order_id
        }
        api = XCoinAPI(self.CLIENT_ID,self.CLIENT_SECRET)
        response = api.xcoinApiCall(endpoint, rgParams)
        return response
