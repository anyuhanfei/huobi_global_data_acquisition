import time

import __init__ as init
from config import config


def combination_data(币种对, 数据):
    '''整合数据
    将已知数据整合成指定格式
    Agrs:
        币种对: 币种
        数据: 从接口中返回的数据，字典类型
    Return:
        dict 已整合的数据
    '''
    add_dict = {}
    add_dict['code'] = 币种对
    add_dict['name'] = 币种对
    add_dict['date'] = time.strftime('%Y-%m-%d')
    add_dict['time'] = time.strftime('%H:%M')
    add_dict['timestamp'] = int(time.time())
    add_dict['data'] = []

    for i in 数据['data']:
        add_dict['data'].append({
            'dt': i['data'][0]['ts'],
            'dc': i['data'][0]['direction'],
            'amount': i['data'][0]['amount'],
            'price': i['data'][0]['price']
        })
    return add_dict


def get_data(币种对):
    '''获取实时成交数据
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    币种对格式替换 = init.币种对格式替换(币种对, '/', '')
    # 获取返回结果
    实时成交URL = init.实时成交URL % (币种对格式替换)
    数据 = init.访问URL(实时成交URL, 'get')
    if 数据 == {} or 'data' in 数据 is False:
        print('获取实时成交数据:%s实时成交数据获取失败' % (币种对))
        return None
    # 组合数据
    add_dict = combination_data(币种对, 数据)
    # 储存和发布
    if config.推送存储方式 == 'redis':
        add_data_redis(币种对, add_dict)
    elif config.推送存储方式 == 'mysql':
        add_data_mysql(add_dict)
    else:
        print('获取实时成交数据:数据存储类型错误')


def add_data_redis(币种对, 数据):
    '''将数据存储到redis
    Agrs:
        币种对: 货币类型
        数据: 已整理数据，字典类型
    '''
    from config import redis连接
    # 发布和存储
    if config.合约开关 is True:
        if config.合约_publish_实时成交 != '':
            redis连接.合约REDIS.publish(config.合约_publish_实时成交, str(数据).replace("'", '"').encode())
        if config.合约_set_实时成交 != '':
            redis连接.合约REDIS.set(config.合约_set_实时成交 % (币种对), str(数据).encode())
    if config.币币开关 is True:
        if config.币币_publish_实时成交 != '':
            redis连接.币币REDIS.publish(config.币币_publish_实时成交, str(数据).replace("'", '"').encode())
        if config.币币_set_实时成交 != '':
            redis连接.币币REDIS.set(config.币币_set_实时成交 % (币种对), str(数据).encode())


def add_data_mysql(coin_type):
    pass
