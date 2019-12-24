import time

import __init__


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
    add_dict['timestamp'] = time.time() * 1000
    add_dict['data'] = []
    for i in content['data']:
        add_dict['data'].append({
            'dt': i['data'][0]['ts'],
            'dc': i['data'][0]['direction'],
            'amount': i['data'][0]['amount'],
            'price': i['data'][0]['price']
        })
    return add_dict


def get_trader_redis(coin_type):
    '''获取实时成交数据
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    from config import redis_conn

    # 处理参数  NAME/NAME -> namename
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '/', '')
    # 获取返回结果
    get_trader_url = __init__.get_trader_url % (coin_type_dispose)
    get_trader_content = __init__.get_url(get_trader_url, 'get')
    if get_trader_content == {}:
        print('实时成交数据获取失败')
        return None
    # 组合数据
    add_dict = combination_data(coin_type, get_trader_content)
    # 发布和存储
    redis_conn.REDIS.publish('vb:trader:chan:mobei', str(add_dict).encode())
    redis_conn.REDIS.set('vb:trader:newitem:', str(add_dict).encode())


def get_trader_mysql(coin_type):
    pass
