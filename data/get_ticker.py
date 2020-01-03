import time

import __init__


def combination_data(coin_type, content, usdt_price):
    '''整合数据
    将已知数据整合成指定格式
    Agrs:
        coin_type: 币种
        content: 从接口中返回的数据，字典类型
        usdt_price: 当前usdt兑换人民币的价格
    Return:
        dict 已整合的数据
    '''
    add_dict = {
        'code': coin_type,
        'name': coin_type,
        'date': time.strftime('%Y-%m-%d'),
        'time': time.strftime('%H:%M'),
        'timestamp': time.time() * 1000,
        'price': content['tick']['close'],
        'cnyPrice': content['tick']['close'] * float(usdt_price.decode()),  # 这里是要获取usdt的价格
        'open': content['tick']['open'],
        'close': content['tick']['close'],
        'high': content['tick']['high'],
        'low': content['tick']['low'],
        'volume': content['tick']['amount'],
        'change': content['tick']['close'] - content['tick']['open'],
        'changeRate': round((content['tick']['close'] - content['tick']['open']) / content['tick']['open'] * 100, 2),
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
        __init__.add_log('data', 'get_ticker', '实时行情获取失败', 0)
        return None
    # 储存和发布
    if __init__.DATABASE_TYPE == 'redis':
        get_ticker_redis(coin_type, get_ricker_content)
    elif __init__.DATABASE_TYPE == 'mysql':
        get_ticker_mysql(get_ricker_content)
    else:
        __init__.add_log('data', 'get_ticker', '数据存储类型错误', 0)


def get_ticker_redis(coin_type, data):
    '''将数据存储到redis
    获取到usdt兑换cny的比例，然后组合数据，将组合完成的数据加入到redis中
    Agrs:
        coin_type: 货币类型
        data: 未整理数据，字典类型
    '''
    from config import redis_conn

    # 组合数据
    usdt_price = redis_conn.REDIS['vb:indexTickerAll:usd2cny']
    add_dict = combination_data(coin_type, data, usdt_price)
    # 发布和储存
    redis_conn.REDIS.publish('vb:ticker:chan:mobei', str(add_dict).encode())
    redis_conn.REDIS.set('vb:ticker:newitem:', str(add_dict).encode())


def get_ticker_mysql(coin_type):
    '''实时行情获取(mysql)'''
    from config import mysql_conn
    print(mysql_conn.CURSOR)
