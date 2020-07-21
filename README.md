# Mine Digital Exchange - Python client
Python client for Mine Digital Exchange API https://minedigital.exchange/

---
A simple python client for Mine Digital Exchange API. Not all API calls have been implemented. Official documentation can be found at:  https://minedigitalexchange.docs.apiary.io

---
## Installation
Clone the Git repository:
```
git clone https://github.com/St0n3M0nKeY/MineDigitalExchange.git
```
Go to the folder of the cloned repository and run:
```
python setup.py install
```
Run Python and import the Mine Digital client.

## Dependencies
Install libs
```
pip install -r .\requirements.txt
```

## Usage - REST API - Public
List of supported currency and currency pairs
```
import minedigital 

mine = minedigital.MineAPI(None, None)

print(mine.get_currencyStatic())
```

## Usage - REST API - Private
Account Information
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.get_account())
```

Trade history
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.get_trade_history(max_results, offset)) # 10, 0
```

List of orders
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.get_orders(active_orders, max_results, offset)) #False, 10, 0
```

Place an order
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.order_new(limit, settlementCurrency, tradedCurrency, price, amount, side)) #"LIMIT", "AUD", "BTC", 16000, 0.01, False
```

Order information
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.order_info(orderId)) #276412403
```

Cancel an order
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.order_cancel([orderId])) # Passed as a list
```

Transactions
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.get_transactions(currency, from_timestamp, to_timestamp, max_results, offset, TransactionState)) # ("BTC", 1464675012000, 1464679012000, 50, 0, "PROCESSED")
```

Retail Quote (RFQ)
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.retail_quote(limit, settlementCurrency, tradedCurrency, price, amount, side, isIndicativeQuote, customRef)) 
#"LIMIT", "AUD", "BTC", 16000, 0.01, False, True, "565f2cdf-3f34-4881-bc80-46584c2c6b8d"
```

Retail Trade (RFQ)
```
import minedigital 

mine = minedigital.MineAPI(api_key, api_secret)

print(mine.retail_trade(quoteId, customRef, amount))
#quoteId(from retail/quote), "565f2cdf-3f34-4881-bc80-46584c2c6b8d", 0.01
```

## Usage - Streaming API - Public
Get orderbook data
```
import minedigital

mine = minedigital.MineSocketio()

mine.register("public/orderBook/ANX/BTCUSD") # market=ANX ccypair=BTCUSD

while True:
    print(mine.data)
```

Get tick data
```
import minedigital

mine = minedigital.MineSocketio()

mine.register("public/tick/ANX/BTCUSD") # market=ANX ccypair=BTCUSD

while True:
    print(mine.data)
```

## Compatibility

This code has been tested on:

- Python 2.7.16
- Python 3.7.2


## TODO

- Implement all API calls available for Mine digital Exchange.
