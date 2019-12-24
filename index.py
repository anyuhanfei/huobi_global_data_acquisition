'''
火币网交易所数据爬虫
'''

from data import get_usdt_cny
from data import get_ticker
from data import get_depth
from data import get_trader
from data import get_depth_pct
from data import get_new_price

from data import goods_kline


# get_usdt_cny.get_usdt_cny_redis()
# get_ticker.get_ticker_redis('BTC/USDT')
# get_depth.get_depth_redis('BTC/USDT')
# get_trader.get_trader_redis('BTC/USDT')
# get_depth_pct.get_depth_pct_redis('BTC/USDT')
# get_new_price.get_new_price_redis('BTC/USDT')
goods_kline.timekeeping('BTC_USDT')
