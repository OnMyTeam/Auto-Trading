import sys, os, calendar
# print(sys.path)
sys.path.append("F:\\BitCoinDev")
from autotrading.db.mongodb import mongodb_handler
from datetime import datetime
from autotrading.machine.bithumb_machine import BithumbMachine
# cur_dir = os.path.abspath(os.curdir)

if __name__== "__main__":
    result_list =[]

    bithumb = BithumbMachine()

    TRADE_CURRENCY_TYPE_list = bithumb.TRADE_CURRENCY_TYPE
    for currency in TRADE_CURRENCY_TYPE_list[:-1]:
        currency_dict = {'cointype':currency}
        filled_orders_list = bithumb.get_filled_orders(currency_type=currency)  # type: object
        if filled_orders_list['status'] != '0000':
            print('오류')
            break
        else:
            filled_orders_list = filled_orders_list['data']
            filled_orders0 = filled_orders_list[0]
            filled_orders1 = filled_orders_list[1]
            filled_orders2 = filled_orders_list[2]
            filled_orders0['cointype']=currency
            filled_orders1['cointype']=currency
            filled_orders2['cointype']=currency

            result_list += [filled_orders0,filled_orders1,filled_orders2]




    mongodb = mongodb_handler.MongoDBHandler("local", "coiner", "price_info")


    """
        item['Currency_Trade'] = 거래소명
        item['year'] = 년도
        item['month'] = 월
        item['day'] = 일
        item['hour'] = 시간
        item['minute'] = 분
        item['second'] = 초
        item['type'] = 매수/매도(ask:판매, bid:구매)
        item['amount'] = 거래 Currency 수량
        item['price'] = 1 Currency 거래 금액
        item['total'] = 총 거래금액
        item['timestamp'] = 체결시간(timestamp) 
    """
    for item in result_list:
        transaction_date = datetime.strptime(item['transaction_date'], '%Y-%m-%d %H:%M:%S')
        item['Currency_Trade'] = 'Bithumb'
        item['year'] = transaction_date.year
        item['month'] = transaction_date.month
        item['day'] = transaction_date.day
        item['hour'] = transaction_date.hour
        item['minute'] = transaction_date.minute
        item['second'] = transaction_date.second
        item['type'] = item['type']
        item['amount'] = item['units_traded']
        item['price'] = item['price']
        item['total'] = item['total']
        item['timestamp'] = transaction_date.timestamp()

        # item['timestamp'] = transaction_date
        ids = mongodb.insert_item(item)
    else:

        print('Success!')







