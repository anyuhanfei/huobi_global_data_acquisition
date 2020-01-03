import redis

import __init__


try:
    REDIS = redis.Redis(host=__init__.REDIS_HOST, port=__init__.REDIS_PORT, password=__init__.REDIS_PASSWROD)
except BaseException:
    print('redis连接失败')
