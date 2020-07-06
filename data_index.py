'''
火币网交易所数据爬虫
'''
import multiprocessing
import time

from utils import CNY汇率
from utils import 实时行情
from utils import 盘口
from utils import 实时成交
from utils import 深度图
from utils import 最新价格

from config import config


def get_data(币种对):
    while True:
        开始时间 = time.time()
        实时行情.get_data(币种对)
        盘口.get_data(币种对)
        实时成交.get_data(币种对)
        深度图.get_data(币种对)
        最新价格.get_data(币种对)
        结束时间 = time.time()
        执行时间 = 结束时间 - 开始时间
        time.sleep(0 if 执行时间 > config.推送间隔时间 else config.推送间隔时间 - 执行时间)
        print('over')


def coin_cny_get():
    while True:
        CNY汇率.CNY汇率()
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
    for 币种对 in config.推送币种对:
        child_process = multiprocessing.Process(target=get_data, args=(币种对, ))
        child_process.daemon = True
        jobs.append(child_process)
        child_process.start()
        time.sleep(config.推送间隔时间 / len(config.推送币种对))
    while True:
        command = input('退出请输入out:')
        if command == 'out':
            break
