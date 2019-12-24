import __init__


def get_usdt_cny_redis():
    '''获取USDT汇率(redis)'''
    from config import redis_conn

    content = __init__.get_url(__init__.get_usdt_cny_url, 'get')
    if content == {}:
        print('USDT汇率获取失败')
        return None
    for i in content['data']:
        if i['name'] == 'usd_cny':
            redis_conn.REDIS.set('vb:indexTickerAll:usd2cny', i['rate'])
        if i['name'] == 'btc_cny':
            redis_conn.REDIS.set('vb:indexTickerAll:btc2cny', i['rate'])


def get_usdt_cny_mysql():
    '''获取USDT汇率(mysql)'''
    pass
