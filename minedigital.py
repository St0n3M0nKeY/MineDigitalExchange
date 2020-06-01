import base64
import hashlib
import hmac
import time
import json
import requests
import socketio

class MineAPI:

    def __init__(self, key, secret):
        self.base_url = 'https://trade.minedigital.exchange/'
        if key is not None and secret is not None:
            self.__key = key
            self.__secret = base64.b64decode(secret)

    def gen_tonce(self):
        return str(int(time.time() * 1e6))

    def get_request(self, path):
        try:
            return requests.get(self.base_url + path).json()
        except Exception as error:
            print("SERVER ERROR GET REQUEST: %s" % error)
            return False

    def post_request(self, path, data):
        try:
            message = (path + chr(0) + data).encode()
            hmac_obj = hmac.new(self.__secret, message, hashlib.sha512)
            hmac_sign = base64.b64encode(hmac_obj.digest())

            header = {
                'Content-Type': 'application/json',
                'User-Agent': '',
                'Rest-Key': self.__key,
                'Rest-Sign': hmac_sign,
            }

            response = requests.post(self.base_url + path, data, headers=header, verify=True)
            json_resp = response.json()
            return json_resp
        except Exception as error:
            print("SERVER ERROR POST REQUEST: %s" % error)
            return False

    def get_account(self):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/account/resource
        path = "api/3/account"
        params = {}
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def order_new(self, limit, settlementCurrency, tradedCurrency, price, amount, side):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/trading/resource
        path = "api/3/order/new"
        params = {}
        params['order'] = {}
        params['order']['orderType'] = limit
        params['order']['settlementCurrency'] = settlementCurrency  
        params['order']['tradedCurrency'] = tradedCurrency
        params['order']['limitPriceInSettlementCurrency'] = price
        params['order']['tradedCurrencyAmount'] = amount
        params['order']['buyTradedCurrency'] = side
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def order_info(self, order_id):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/trading/resource-2
        path = "api/3/order/info"
        params = {}
        params['orderId'] = order_id
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def order_cancel(self, order_id):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/trading/resource-3
        path = "api/3/order/cancel"
        params = {}
        params['orderIds'] = order_id
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def get_transactions(self, currency, from_timestamp, to_timestamp, max_results, offset, TransactionState):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/activities/resource
        path = "api/3/transaction/list"
        params = {}
        params['tonce'] = self.gen_tonce()
        params['ccy'] = currency 
        params['transactionState'] = TransactionState
        params['from'] = from_timestamp
        params['to'] = to_timestamp 
        params['max'] = max_results 
        params['offset'] = offset
        params['lang'] = "en-US"
        return self.post_request(path, json.dumps(params))
    
    def get_orders(self, active_orders, max_results, offset):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/activities/resource-2
        path = "api/3/order/list"
        params = {}
        params['tonce'] = self.gen_tonce()
        params['activeOnly'] = active_orders
        params['max'] = max_results 
        params['offset'] = offset 
        return self.post_request(path, json.dumps(params))

    def get_trade_history(self, max_results, offset):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/activities/resource-3
        path = "api/3/trade/list"
        params = {}
        params['tonce'] = self.gen_tonce()
        params['max'] = max_results 
        params['offset'] = offset
        return self.post_request(path, json.dumps(params))

    def retail_quote(self, limit, settlementCurrency, tradedCurrency, price, amount, side, isIndicativeQuote, customRef):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/retail-trading
        path = "api/3/retail/quote"
        params = {}
        params['quoteRequest'] = {}
        params['quoteRequest']['orderType'] = limit
        params['quoteRequest']['settlementCurrency'] = settlementCurrency
        params['quoteRequest']['tradedCurrency'] = tradedCurrency
        params['quoteRequest']['limitPriceInSettlementCurrency'] = price
        params['quoteRequest']['tradedCurrencyAmount'] = amount
        params['quoteRequest']['buyTradedCurrency'] = side
        params['quoteRequest']['isIndicativeQuote'] = isIndicativeQuote
        params['quoteRequest']['customRef'] = customRef
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def retail_trade(self, quoteId, customRef, amount):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/retail-trading
        path = "api/3/retail/trade"
        params = {}
        params['tradeRequest'] = {}
        params['tradeRequest']['quoteId'] = quoteId
        params['tradeRequest']['customRef'] = customRef
        params['tradeRequest']['amount'] = amount
        params['tonce'] = self.gen_tonce()
        return self.post_request(path, json.dumps(params))

    def get_currencyStatic(self):
        #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/supported-currency-and-currency-pair/resource
        path = "api/3/currencyStatic"
        return self.get_request(path)


class MineSocketio():
    #https://minedigitalapidocumentationv1.docs.apiary.io/#/reference/streaming

    def __init__(self):
        self.data = ''
        self.url = 'https://trade.minedigital.exchange:443'
        self.params = {"path": "/streaming/3", "rejectUnauthorized": "false", "transports": 'websocket', "agent": "false", "upgrade": "false"}
        self.sio = socketio.Client(logger=True)

    def register(self, path):
        try:
            self.sio.connect(self.url, self.params)
            self.sio.emit('subscribe', path)
            self.sio.on(path, self.on_message)
        except:
            self.sio.disconnect()

    def get_sid(self):
        return self.sio.sid

    def on_message(self, *args):
        self.set_message(args)

    def set_message(self, args):
        self.data = args
