import redis

import __init__


try:
    REDIS = redis.Redis(host=__init__.REDIS_HOST, port=__init__.REDIS_PORT)
except BaseException:
    print('redis连接失败')
