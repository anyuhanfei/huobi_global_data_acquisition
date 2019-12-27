'''
火币网交易所数据爬虫
'''

from data import get_usdt_cny
from data import get_ticker
from data import get_depth
from data import get_trader
from data import get_depth_pct
from data import get_new_price

import __init__

while True:
    get_usdt_cny.get_usdt_cny_redis()
    for coin_type in __init__.COIN_TYPE:
        get_ticker.get_ticker_redis(coin_type)
        get_depth.get_depth_redis(coin_type)
        get_trader.get_trader_redis(coin_type)
        get_depth_pct.get_depth_pct_redis(coin_type)
        get_new_price.get_new_price_redis(coin_type)
    print(1)
