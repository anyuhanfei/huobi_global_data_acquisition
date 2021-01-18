import requests
import json
import os
import sys
import time

from config import config














'''数据地址和API接口'''
实时行情URL = 'https://api.huobipro.com/market/detail/merged?symbol=%s'
CNY汇率URL = "https://www.hbg.com/-/x/general/exchange_rate/list?r=86xktl2lldf"
盘口URL = 'https://api.huobipro.com/market/depth?symbol=%s&type=step0'
实时成交URL = 'https://api.huobipro.com/market/history/trade?symbol=%s&size=50'
深度图URL = 'https://api.huobipro.com/market/depth?symbol=%s&type=step0'
最新价格URL = 'https://api.huobipro.com/market/detail/merged?symbol=%s'
K线图URL = 'https://api.huobipro.com/market/history/kline?period=%s&size=' + str(config.K线图获取数量) + '&symbol=%s'


"""
系统全局方法
"""


def 币种对格式替换(search, str1, str2):
    '''替换指定字符并将字符串转化为小写'''
    return search.replace(str1, str2).lower()


def 访问URL(url, http_type, headers='', cookies=''):
    if headers == '':
        headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    if cookies == '':
        cookies = {'__cfduid': "dee69a04290259373c4aa10d8316c5b951578028289"}
    try:
        res = requests.get(url, timeout=10, headers=headers, cookies=cookies)
    except BaseException as e:
        print('url:%s:%s' % (url, e))
        return {}
    if res.status_code == 200:
        return json.loads(res.content.decode())
    else:
        return {}


def write_log(数据, 币种对, 数据类型, 交易类型):
    if config.日志开关 is False:
        return None
    coin = 币种对.replace('/', '').replace('_', '')
    time_log_path = '{}.log'.format(time.strftime('%Y%m%d-%H'))
    log_path = '{path}/log/{交易类型}/{数据类型}/{coin}'.format(path=sys.path[0], 交易类型=交易类型, 数据类型=数据类型, coin=coin)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    with open(log_path + '/' + time_log_path, 'a', encoding='utf8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        f.write(数据 + '\n')
