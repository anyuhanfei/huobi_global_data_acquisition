import __init__


def get_new_price_redis(coin_type):
    '''获取最新价格
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    from config import redis_conn

    # 处理参数  NAME/NAME -> namename
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '/', '')
    # 获取返回结果
    get_new_price_url = __init__.get_new_price_url % (coin_type_dispose)
    get_new_price_content = __init__.get_url(get_new_price_url, 'get')
    if get_new_price_content == {}:
        print('最新价格获取失败')
        return None
    # 存储
    redis_conn.REDIS.set('vb:depth:newitem:%s' % (coin_type), get_new_price_content['tick']['close'])


def get_new_price_mysql(coin_type):
    pass
