import time
import json

import __init__
from config import redis_conn


def combination_data(coin_type, content, cny_price):
    '''整合数据
    将已知数据整合成指定格式
    Agrs:
        coin_type: 币种
        content: 从接口中返回的数据，字典类型
        cny_price: 当前币种兑换人民币的价格
    Return:
        dict 已整合的数据
    '''
    try:
        风控_number = float(redis_conn.REDIS['%s%s' % (__init__.风控_KEY, coin_type)].decode()) if (__init__.使用风控 is True) else 0
    except BaseException:
        风控_number = 0
    add_dict = {
        'code': coin_type,
        'name': coin_type,
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M'),
        'timestamp': int(time.time()),
        'price': content['tick']['close'] + 风控_number,
        'cnyPrice': (content['tick']['close'] + 风控_number) * cny_price,  # 这里是要获取usdt的价格
        'open': content['tick']['open'] + 风控_number,
        'close': content['tick']['close'] + 风控_number,
        'high': content['tick']['high'] + 风控_number,
        'low': content['tick']['low'] + 风控_number,
        'volume': content['tick']['amount'],
        'change': content['tick']['close'] - content['tick']['open'],
        'changeRate': str(round((content['tick']['close'] - content['tick']['open']) / content['tick']['open'] * 100, 2)) + '%',
        'buy': content['tick']['bid'][0],
        'sell': content['tick']['ask'][0]
    }
    return add_dict


def get_ticker(coin_type):
    '''实时行情获取
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '/', '')
    # 获取返回结果
    get_ricker_url = __init__.get_ticker_url % (coin_type_dispose)
    get_ricker_content = __init__.get_url(get_ricker_url, 'get')
    if get_ricker_content == {}:
        print('实时行情获取:%s实时行情获取失败' % (coin_type))
        return None
    # 储存和发布
    if __init__.DATABASE_TYPE == 'redis':
        get_ticker_redis(coin_type, get_ricker_content)
    elif __init__.DATABASE_TYPE == 'mysql':
        get_ticker_mysql(get_ricker_content)
    else:
        print('实时行情获取:数据存储类型错误')


def get_ticker_redis(coin_type, data):
    '''将数据存储到redis
    获取到usdt兑换cny的比例，然后组合数据，将组合完成的数据加入到redis中
    Agrs:
        coin_type: 货币类型
        data: 未整理数据，字典类型
    '''
    coin = coin_type.split('/')
    if coin[1] == 'USDT':
        cny_price = float(redis_conn.REDIS['vb:indexTickerAll:usd2cny'].decode())
    elif coin[1] == 'BTC':
        cny_price = float(redis_conn.REDIS['vb:indexTickerAll:btc2cny'].decode())
    else:
        cny_price = json.loads(redis_conn.REDIS["vb:ticker:newitem:ETH/USDT"].decode().replace("\'", "\""))['cnyPrice']
    # 组合数据
    add_dict = combination_data(coin_type, data, cny_price)
    # 发布和储存
    if __init__.推送_通道_行情 != '':
        redis_conn.REDIS.publish(__init__.推送_通道_行情, str(add_dict).replace("'", '"').encode())
    if __init__.推送_合约_行情 != '':
        redis_conn.REDIS.set(__init__.推送_合约_行情 % (coin_type), str(add_dict).encode())


def get_ticker_mysql(coin_type):
    '''实时行情获取(mysql)'''
    from config import mysql_conn
    print(mysql_conn.CURSOR)
