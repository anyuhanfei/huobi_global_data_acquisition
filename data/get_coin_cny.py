import __init__


def get_coin_cny():
    '''获取币种兑换人民币汇率'''
    content = __init__.get_url(__init__.get_coin_cny_url, 'get')
    if content == {}:
        __init__.add_log('data', 'get_coin_cny', '汇率获取失败', 0)
        return None
    if __init__.DATABASE_TYPE == 'redis':
        get_coin_cny_redis(content)
    elif __init__.DATABASE_TYPE == 'mysql':
        get_coin_cny_mysql(content)
    else:
        __init__.add_log('data', 'get_coin_cny', '数据存储类型错误', 0)


def get_coin_cny_redis(data):
    '''将数据存储到redis
    Agrs:
        data: 接口返回数据，字典类型
    '''
    from config import redis_conn

    for i in data['data']:
        if i['name'] == 'usdt_cny':
            print(i['rate'])
            redis_conn.REDIS.set('vb:indexTickerAll:usd2cny', i['rate'])
        if i['name'] == 'btc_cny':
            redis_conn.REDIS.set('vb:indexTickerAll:btc2cny', i['rate'])


def get_coin_cny_mysql():
    '''获取USDT汇率(mysql)'''
    pass
