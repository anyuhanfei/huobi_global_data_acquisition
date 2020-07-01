'''
火币网交易所数据爬虫
'''
import multiprocessing
import time

from utils import get_coin_cny
from utils import get_ticker
from utils import get_depth
from utils import get_trader
from utils import get_depth_pct
from utils import get_new_price

import __init__


def get_data(coin_type):
    while True:
        start_time = time.time()
        get_ticker.get_ticker(coin_type)
        get_depth.get_depth(coin_type)
        get_trader.get_trader(coin_type)
        get_depth_pct.get_depth_pct(coin_type)
        get_new_price.get_new_price(coin_type)
        end_time = time.time()
        execution_time = end_time - start_time
        time.sleep(0 if execution_time > __init__.GET_DATA_INTERVAL_TIME else __init__.GET_DATA_INTERVAL_TIME - execution_time)


def coin_cny_get():
    while True:
        get_coin_cny.get_coin_cny()
        time.sleep(0.4)


if __name__ == '__main__':
    jobs = []
    # 获取币种兑换cny的比例
    child_process = multiprocessing.Process(target=coin_cny_get)
    child_process.daemon = True
    jobs.append(child_process)
    child_process.start()
    time.sleep(0.1)
    # 循环币种设置子进程
    for coin_type in __init__.COIN_TYPE:
        child_process = multiprocessing.Process(target=get_data, args=(coin_type, ))
        child_process.daemon = True
        jobs.append(child_process)
        child_process.start()
        time.sleep(__init__.GET_DATA_INTERVAL_TIME / len(__init__.COIN_TYPE))
    while True:
        command = input('退出请输入out:')
        if command == 'out':
            break
