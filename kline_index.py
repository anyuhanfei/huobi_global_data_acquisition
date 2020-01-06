'''
火币网交易所K线图爬虫
'''
import multiprocessing
import time

import __init__
from data import goods_kline


if __name__ == "__main__":
    jobs = []
    for coin_type in __init__.COIN_TYPE_KLINE:
        number = (len(jobs) % len(__init__.COIN_TYPE_KLINE)) + 1
        child_process = multiprocessing.Process(target=goods_kline.timekeeping, args=(coin_type, number,))
        child_process.daemon = True
        jobs.append(child_process)
        child_process.start()
        time.sleep(0.1)
    while True:
        command = input('退出请输入out:')
        if command == 'out':
            break
