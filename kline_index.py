'''
火币网交易所K线图爬虫
'''
import multiprocessing
import time

from config import config
from utils import k
from config import mysql连接


if __name__ == "__main__":
    jobs = []
    for coin_type in config.K线图币种对:
        number = (len(jobs) % len(config.K线图币种对)) + 1
        child_process = multiprocessing.Process(target=k.timekeeping, args=(coin_type, number, mysql连接.MYSQL连接(), ))
        child_process.daemon = True
        jobs.append(child_process)
        child_process.start()
        time.sleep(0.1)
    while True:
        command = input('退出请输入out:')
        if command == 'out':
            break
