import requests
import json
import time
import os

"""
系统全局配置
"""
'''get data interval time'''
GET_DATA_INTERVAL_TIME = 0.5


'''coin type'''
COIN_TYPE = [
    'BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'BCH/USDT', 'EOS/USDT', 'EOS/ETH', 'ADA/ETH', 'OMG/ETH',
    'LTC/BTC', 'BCH/BTC', 'ETH/BTC', 'EOS/BTC', 'XRP/BTC', 'ETC/BTC'
]

COIN_TYPE_KLINE = [
    'BTC_USDT', 'ETH_USDT', 'XRP_USDT', 'LTC_USDT', 'BCH_USDT', 'EOS_USDT', 'EOS_ETH', 'ADA_ETH', 'OMG_ETH',
    'LTC_BTC', 'BCH_BTC', 'ETH_BTC', 'EOS_BTC', 'XRP_BTC', 'ETC_BTC'
]

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
MYSQL_DBNAME = 'exchange_reptile'
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
        add_log('url', 'url', e)
        return {}
    if res.status_code == 200:
        return json.loads(res.content.decode())
    else:
        return {}


def add_log(type, coin_type, content, level=0):
    '''添加日志记录
    每天的日志单独记录，存放在当前月份命名的目录下
    Agrs:
        type: 日志类型
        content: 日志内容
        level: 日志层级，0表示顶级，每增加一级多4个空格
    '''
    # 获取需要用到的时间
    new_time = time.strftime("%Y-%m-%d %H:%M:%S")
    new_month = time.strftime("%Y-%m")
    new_day = time.strftime("%Y-%m-%d")
    # 一级目录的检测与创建
    log_dir_name = 'log/%s' % (type)
    if not os.path.exists(log_dir_name):
        os.makedirs(log_dir_name)
    # 二级目录的检测与创建
    log_dir_name = 'log/%s/%s' % (type, coin_type)
    if not os.path.exists(log_dir_name):
        os.makedirs(log_dir_name)
    # 三级目录的检测与创建
    log_dir_name = 'log/%s/%s/%s' % (type, coin_type, new_month)
    if not os.path.exists(log_dir_name):
        os.makedirs(log_dir_name)
    # 文件写入
    res_content = '%s%s  (%s)\n' % ('    ' * level, content, new_time)
    log_file_name = '%s/%s.log' % (log_dir_name, new_day)
    with open(log_file_name, 'a+', encoding='utf-8') as f:
        f.write(res_content)
