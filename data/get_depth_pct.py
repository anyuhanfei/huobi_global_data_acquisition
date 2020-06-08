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
    from config import redis_conn

    add_dict = {}
    add_dict['code'] = coin_type
    add_dict['name'] = coin_type
    add_dict['date'] = time.strftime('%Y-%m-%d')
    add_dict['time'] = time.strftime('%H:%M')
    add_dict['timestamp'] = int(time.time())
    add_dict['bids'] = []
    bids = 0
    try:
        风控_number = float(redis_conn.REDIS['%s%s' % (__init__.风控_KEY, coin_type)].decode()) if (__init__.使用风控 is True) else 0
    except BaseException:
        风控_number = 0
    for i in range(0, 200 if len(content['tick']['bids']) >= 200 else len(content['tick']['bids'])):
        bids += round(content['tick']['bids'][i][1], 2)
        add_dict['bids'].append({
            'totalSize': bids,
            'price': round(content['tick']['bids'][i][0] + 风控_number, 2)
        })
    add_dict['asks'] = []
    asks = 0
    for i in range(0, 200 if len(content['tick']['asks']) >= 200 else len(content['tick']['asks'])):
        asks += round(content['tick']['asks'][i][1], 2)
        add_dict['asks'].append({
            'totalSize': asks,
            'price': round(content['tick']['asks'][i][0] + 风控_number, 2)
        })
    return add_dict


def get_depth_pct(coin_type):
    '''获取深度图数据
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '/', '')
    # 获取返回结果
    get_depth_pct_url = __init__.get_depth_pct_url % (coin_type_dispose)
    get_depth_pct_content = __init__.get_url(get_depth_pct_url, 'get')
    if get_depth_pct_content == {}:
        print('获取深度图数据:%s深度图数据获取失败' % (coin_type))
        return None
    # 组合数据
    add_dict = combination_data(coin_type, get_depth_pct_content)
    # 储存和发布
    if __init__.DATABASE_TYPE == 'redis':
        add_data_redis(coin_type, add_dict)
    elif __init__.DATABASE_TYPE == 'mysql':
        add_data_mysql(coin_type, add_dict)
    else:
        print('获取深度图数据:数据存储类型错误')


def add_data_redis(coin_type, add_data):
    '''将数据存储到redis
    数据转换为json字符串，然后分别添加到通道和存储中
    Agrs:
        add_dict: 已整理数据，字典类型
    '''
    from config import redis_conn
    res_add_data = str(add_data).replace("'", '"').encode()
    redis_conn.REDIS.publish('vb:depth:pct:chan:mobei', res_add_data)
    redis_conn.REDIS.set('vb:depth:pct:newitem:%s' % (coin_type), res_add_data)


def add_data_mysql(coin_type, add_data):
    pass
