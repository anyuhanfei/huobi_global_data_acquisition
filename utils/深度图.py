import time

import __init__ as init
from config import config


def combination_data(coin_type, content):
    '''整合数据
    将已知数据整合成指定格式
    Agrs:
        coin_type: 币种
        content: 从接口中返回的数据，字典类型
    Return:
        dict 已整合的数据
    '''
    add_dict = {}
    add_dict['code'] = coin_type
    add_dict['name'] = coin_type
    add_dict['date'] = time.strftime('%Y-%m-%d')
    add_dict['time'] = time.strftime('%H:%M')
    add_dict['timestamp'] = int(time.time())
    add_dict['bids'] = []
    bids = 0
    for i in range(0, 200 if len(content['tick']['bids']) >= 200 else len(content['tick']['bids'])):
        bids += round(content['tick']['bids'][i][1], 2)
        add_dict['bids'].append({
            'totalSize': bids,
            'price': round(content['tick']['bids'][i][0], 5)
        })
    add_dict['asks'] = []
    asks = 0
    for i in range(0, 200 if len(content['tick']['asks']) >= 200 else len(content['tick']['asks'])):
        asks += round(content['tick']['asks'][i][1], 2)
        add_dict['asks'].append({
            'totalSize': asks,
            'price': round(content['tick']['asks'][i][0], 5)
        })
    return add_dict


def get_data(币种对):
    '''获取深度图数据
    Agrs:
        币种对: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    币种对格式替换 = init.币种对格式替换(币种对, '/', '')
    # 获取返回结果
    深度图URL = init.深度图URL % (币种对格式替换)
    数据 = init.访问URL(深度图URL, 'get')
    if 数据 == {} or 'tick' in 数据 is False:
        print('获取深度图数据:%s深度图数据获取失败' % (币种对))
        return None
    # 组合数据
    add_dict = combination_data(币种对, 数据)
    # 储存和发布
    if config.推送存储方式 == 'redis':
        add_data_redis(币种对, add_dict)
    elif config.推送存储方式 == 'mysql':
        add_data_mysql(币种对, add_dict)
    else:
        print('获取深度图数据:数据存储类型错误')


def add_data_redis(币种对, add_data):
    '''将数据存储到redis
    数据转换为json字符串，然后分别添加到通道和存储中
    Agrs:
        add_dict: 已整理数据，字典类型
    '''
    from config import redis连接

    if config.合约开关 is True:
        try:
            风控_number = float(redis连接.合约REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        合约add_data = {'bids': [], 'asks': []}
        for bids in add_data['bids']:
            bids['price'] += 风控_number
            合约add_data['bids'].append(bids)
        for asks in add_data['asks']:
            asks['price'] += 风控_number
            合约add_data['asks'].append(asks)
        res_add_data = str(add_data).replace("'", '"').encode()
        if res_add_data:
            if config.合约_publish_深度图 != '':
                redis连接.合约REDIS.publish(config.合约_publish_深度图, res_add_data)
            if config.合约_set_深度图 != '':
                redis连接.合约REDIS.set(config.合约_set_深度图 % (币种对), res_add_data)
    if config.币币开关 is True:
        try:
            风控_number = float(redis连接.币币REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        币币add_data = {'bids': [], 'asks': []}
        for bids in add_data['bids']:
            bids['price'] += 风控_number
            币币add_data['bids'].append(bids)
        for asks in add_data['asks']:
            asks['price'] += 风控_number
            币币add_data['asks'].append(asks)
        res_add_data = str(add_data).replace("'", '"').encode()
        if res_add_data:
            if config.币币_publish_深度图 != '':
                redis连接.币币REDIS.publish(config.币币_publish_深度图, res_add_data)
            if config.币币_set_深度图 != '':
                redis连接.币币REDIS.set(config.币币_set_深度图 % (币种对), res_add_data)


def add_data_mysql(coin_type, add_data):
    pass
