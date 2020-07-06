import redis

from config import config


try:
    if config.合约开关 is True:
        合约REDIS = redis.Redis(host=config.合约_REDIS_HOST, port=config.合约_REDIS_PORT, password=config.合约_REDIS_PASSWROD)
    if config.币币开关 is True:
        币币REDIS = redis.Redis(host=config.币币_REDIS_HOST, port=config.币币_REDIS_PORT, password=config.币币_REDIS_PASSWROD)
except BaseException:
    print('redis连接失败')
