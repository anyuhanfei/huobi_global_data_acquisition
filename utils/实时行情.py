import time
import json

import __init__ as init
from config import config
from config import redis连接


def combination_data(币种对, 数据, cny_price, 交易方式):
    '''整合数据
    将已知数据整合成指定格式
    Agrs:
        币种对: 币种
        数据: 从接口中返回的数据，字典类型
        cny_price: 当前币种兑换人民币的价格
    Return:
        dict 已整合的数据
    '''
    try:
        if 交易方式 == '合约':
            风控_number = float(redis连接.合约REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        if 交易方式 == '币币':
            风控_number = float(redis连接.币币REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
    except BaseException:
        风控_number = 0
    add_dict = {
        'code': 币种对,
        'name': 币种对,
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M'),
        'timestamp': int(time.time()),
        'price': 数据['tick']['close'] + 风控_number,
        'cnyPrice': (数据['tick']['close'] + 风控_number) * cny_price,  # 这里是要获取usdt的价格
        'open': 数据['tick']['open'] + 风控_number,
        'close': 数据['tick']['close'] + 风控_number,
        'high': 数据['tick']['high'] + 风控_number,
        'low': 数据['tick']['low'] + 风控_number,
        'volume': 数据['tick']['amount'],
        'change': 数据['tick']['close'] - 数据['tick']['open'],
        'changeRate': str(round((数据['tick']['close'] - 数据['tick']['open']) / 数据['tick']['open'] * 100, 2)) + '%',
        'buy': 数据['tick']['bid'][0],
        'sell': 数据['tick']['ask'][0]
    }
    return add_dict


def get_data(币种对):
    '''实时行情获取
    Agrs:
        币种对: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    币种对格式替换 = init.币种对格式替换(币种对, '/', '')
    # 获取返回结果
    实时行情URL = init.实时行情URL % (币种对格式替换)
    数据 = init.访问URL(实时行情URL, 'get')
    if 数据 == {} or 'tick' in 数据 is False:
        print('实时行情获取:%s实时行情获取失败' % (币种对))
        return None
    # 储存和发布
    if config.推送存储方式 == 'redis':
        get_ticker_redis(币种对, 数据)
    elif config.推送存储方式 == 'mysql':
        get_ticker_mysql(数据)
    else:
        print('实时行情获取:数据存储类型错误')


def get_ticker_redis(币种对, 数据):
    '''将数据存储到redis
    获取到usdt兑换cny的比例，然后组合数据，将组合完成的数据加入到redis中
    Agrs:
        币种对: 货币类型
        数据: 未整理数据，字典类型
    '''
    coin = 币种对.split('/')
    if config.合约开关 is True:
        if coin[1] == 'USDT':
            cny_price = float(redis连接.合约REDIS[config.USDT2CNY].decode())
        elif coin[1] == 'BTC':
            cny_price = float(redis连接.合约REDIS[config.BTC2CNY].decode())
        else:
            cny_price = json.loads(redis连接.合约REDIS[config.合约_set_实时行情 % ('ETH/USDT')].decode().replace("\'", "\""))['cnyPrice']
        # 组合数据
        add_dict = combination_data(币种对, 数据, cny_price, '合约')
        # 发布和储存
        if config.推送存储方式 != '':
            redis连接.合约REDIS.publish(config.合约_publish_实时行情, str(add_dict).replace("'", '"').encode())
        if config.推送存储方式 != '':
            redis连接.合约REDIS.set(config.合约_set_实时行情 % (币种对), str(add_dict).encode())
    if config.币币开关 is True:
        if coin[1] == 'USDT':
            cny_price = float(redis连接.币币REDIS[config.USDT2CNY].decode())
        elif coin[1] == 'BTC':
            cny_price = float(redis连接.币币REDIS[config.BTC2CNY].decode())
        else:
            cny_price = json.loads(redis连接.币币REDIS[config.币币_set_实时行情 % ('ETH/USDT')].decode().replace("\'", "\""))['cnyPrice']
        # 组合数据
        add_dict = combination_data(币种对, 数据, cny_price, '币币')
        # 发布和储存
        if config.推送存储方式 != '':
            redis连接.币币REDIS.publish(config.币币_publish_实时行情, str(add_dict).replace("'", '"').encode())
        if config.推送存储方式 != '':
            redis连接.币币REDIS.set(config.币币_set_实时行情 % (币种对), str(add_dict).encode())


def get_ticker_mysql(币种对):
    '''实时行情获取(mysql)'''
    from config import mysql_conn
    print(mysql_conn.CURSOR)
