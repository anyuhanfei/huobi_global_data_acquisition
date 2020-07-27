import __init__ as init
from config import config


def CNY汇率():
    '''获取币种兑换人民币汇率'''
    content = init.访问URL(init.CNY汇率URL, 'get')
    if content == {} or 'data' in content is False:
        print('获取币种兑换人民币汇率:汇率获取失败')
        return None
    if config.数据存储方式 == 'redis':
        add_data_redis(content)
    elif config.数据存储方式 == 'mysql':
        add_data_mysql(content)
    else:
        print('获取币种兑换人民币汇率:数据存储类型错误')


def add_data_redis(data):
    '''将数据存储到redis
    Agrs:
        data: 接口返回数据，字典类型
    '''
    from config import redis连接

    for i in data['data']:
        if i['name'] == 'usdt_cny':
            if config.合约开关 is True:
                redis连接.合约REDIS.set(config.USDT2CNY, i['rate'])
            if config.币币开关 is True:
                redis连接.币币REDIS.set(config.USDT2CNY, i['rate'])
        if i['name'] == 'btc_cny':
            if config.合约开关 is True:
                redis连接.合约REDIS.set(config.BTC2CNY, i['rate'])
            if config.币币开关 is True:
                redis连接.币币REDIS.set(config.BTC2CNY, i['rate'])


def add_data_mysql():
    '''获取USDT汇率(mysql)'''
    pass
