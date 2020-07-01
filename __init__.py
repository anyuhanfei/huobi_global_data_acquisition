import requests
import json


"""
系统全局配置
"""
'''get data interval time'''
GET_DATA_INTERVAL_TIME = 1

'''coin type'''
COIN_USDT = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'BCH/USDT', 'EOS/USDT']  # USDT相关币种对
COIN_ETH = ['EOS/ETH', 'ADA/ETH', 'OMG/ETH']  # ETH相关币种对
COIN_BTC = ['LTC/BTC', 'BCH/BTC', 'ETH/BTC', 'EOS/BTC', 'XRP/BTC', 'ETC/BTC']  # BTC相关币种对

# 设置使用的币种对, 加一个空列表是因为防止进行浅复制
COIN_TYPE = [] + COIN_USDT

# K线图使用的币种对, 无需修改
COIN_TYPE_KLINE = [] + COIN_TYPE
for i in range(0, len(COIN_TYPE)):
    COIN_TYPE_KLINE[i] = COIN_TYPE[i].replace('/', '_')

'''use database type'''
DATABASE_TYPE = 'redis'  # redis or mysql

'''redis set'''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_AUTH = ''
REDIS_PASSWROD = ''

'''mysql set'''
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DBNAME = 'k'
MYSQL_CHARSET = 'utf8'

'''visit url'''
VISIT_URL_TIMEOUT = 10  # 访问网址超时时间

'''get kline size'''
GET_KLINE_SIZE = 7

'''url'''
get_ticker_url = 'https://api.huobipro.com/market/detail/merged?symbol=%s'
get_coin_cny_url = "https://www.hbg.com/-/x/general/exchange_rate/list?r=86xktl2lldf"
get_depth_url = 'https://api.huobipro.com/market/depth?symbol=%s&type=step0'
get_trader_url = 'https://api.huobipro.com/market/history/trade?symbol=%s&size=50'
get_depth_pct_url = 'https://api.huobipro.com/market/depth?symbol=%s&type=step0'
get_new_price_url = 'https://api.huobipro.com/market/detail/merged?symbol=%s'
goods_kline_url = 'https://api.huobipro.com/market/history/kline?period=%s&size=' + str(GET_KLINE_SIZE) + '&symbol=%s'

'''redis推送(通道)'''
推送_通道_最新价 = ""
推送_通道_行情 = "contract:vb:ticker:chan:mobei"
推送_通道_深度图 = "contract:vb:depth:pct:chan:mobei"
推送_通道_盘口 = "contract:vb:depth:chan:mobei"
推送_通道_实时行情 = "contract:vb:trader:chan:mobei"

'''redis推送(合约)'''
推送_合约_最新价 = "contract:vb:ticker:newprice:%s"
推送_合约_行情 = "contract:vb:ticker:newitem:%s"
推送_合约_深度图 = "contract:vb:depth:pct:newitem:%s"
推送_合约_盘口 = "contract:vb:depth:newitem:%s"
推送_合约_实时行情 = "contract:vb:trader:newitem:%s"

'''风控'''
使用风控 = True
风控_KEY = 'vb:risk:management:'  # 例: vb:risk:management:GOLD/USDT


"""
系统全局方法
"""


def coin_type_dispose(search, str1, str2):
    '''替换指定字符并将字符串转化为小写'''
    return search.replace(str1, str2).lower()


def get_url(url, http_type, headers='', cookies=''):
    if headers == '':
        headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    if cookies == '':
        cookies = {'__cfduid': "dee69a04290259373c4aa10d8316c5b951578028289"}
    try:
        res = requests.get(url, timeout=VISIT_URL_TIMEOUT, headers=headers, cookies=cookies)
    except BaseException as e:
        print('url:%s:%s' % (url, e))
        return {}
    if res.status_code == 200:
        return json.loads(res.content.decode())
    else:
        return {}
