import __init__ as init
from config import config


def get_data(币种对):
    '''获取最新价格
    Agrs:
        币种对: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    币种对格式替换 = init.币种对格式替换(币种对, '/', '')
    # 获取返回结果
    最新价格URL = init.最新价格URL % (币种对格式替换)
    数据 = init.访问URL(最新价格URL, 'get')
    if 数据 == {} or 'tick' in 数据 is False:
        print('获取最新价格:%s最新价格获取失败' % (币种对))
        return None
    # 储存和发布
    if config.推送存储方式 == 'redis':
        add_data_redis(币种对, 数据)
    elif config.推送存储方式 == 'mysql':
        add_data_mysql(数据)
    else:
        print('获取最新价格:数据存储类型错误')


def add_data_redis(币种对, data):
    '''将数据存储到redis
    Agrs:
        币种对: 货币类型
        data: 已整理数据，字典类型
    '''
    from config import redis连接

    if config.合约开关 is True:
        try:
            风控_number = float(redis连接.合约REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        if config.合约_publish_最新价格 != '':
            redis连接.合约REDIS.publish(config.合约_publish_最新价格, data['tick']['close'] + 风控_number)
        if config.合约_set_最新价格 != '':
            redis连接.合约REDIS.set(config.合约_set_最新价格 % (币种对), data['tick']['close'] + 风控_number)
    if config.币币开关 is True:
        try:
            风控_number = float(redis连接.币币REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        if config.币币_publish_最新价格 != '':
            redis连接.币币REDIS.publish(config.币币_publish_最新价格, data['tick']['close'] + 风控_number)
        if config.币币_set_最新价格 != '':
            redis连接.币币REDIS.set(config.币币_set_最新价格 % (币种对), data['tick']['close'] + 风控_number)


def add_data_mysql(data):
    pass
