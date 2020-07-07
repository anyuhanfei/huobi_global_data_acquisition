import time
import threading

import __init__ as init
from config import config


# 多线程队列
threads = []


def get_data(币种对, K线图类型):
    '''访问接口，获取返回数据
    Agrs:
        币种对: 接口参数二，传来格式为 NAME_NAME，需修改为 namename
        K线图类型: 接口参数一，k线图时间类型
    return:
        dict 接口返回的无修改数据
    '''
    币种对其他格式 = init.币种对格式替换(币种对, '_', '')
    K线图URL = init.K线图URL % (K线图类型, 币种对其他格式)
    数据 = init.访问URL(K线图URL, 'get')
    return 数据


def add_sql(数据, 币种对, K线图类型, MYSQL连接, 交易类型):
    '''添加数据
    Agrs:
        数据: 接口返回数据
        币种对: 参数二，保存数据
        K线图类型: 参数一，根据值获取对应表名
        MYSQL连接: mysql连接对象
        交易类型: 执行sql语句时区分执行哪个数据库连接, 合约或币币
    '''
    select_sql = "select * from %s where  code='%s' and date='%s'" % (
        config.K线图表名[K线图类型],
        币种对.replace('_', '/'),
        time.strftime("%Y-%m-%d %H:%M", time.localtime(数据['data'][0]['id']))
    )
    select_res = MYSQL连接.语句执行(select_sql, 交易类型)
    if select_res == 0:
        content_time = time.localtime(数据['data'][0]['id'])
        add_sql = "insert into %s (%s) value ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            config.K线图表名[K线图类型],
            'code, period, volume, price, opening_price, closing_price, pre_closing_price, highest_price, lowest_price, date_ymd, date, create_time',
            币种对.replace('_', '/'),
            time.strftime("%Y%m%d", content_time),
            round(数据['data'][0]['amount'], 7),  # 成交量
            数据['data'][0]['close'],  # 收盘价
            数据['data'][0]['open'],  # 开盘价
            数据['data'][0]['close'],  # 收盘价
            0,
            数据['data'][0]['high'],  # 最高价
            数据['data'][0]['low'],  # 最低价
            time.strftime("%Y%m%d", content_time),
            time.strftime("%Y-%m-%d %H:%M", content_time),
            time.strftime("%Y-%m-%d %H:%M:%S", content_time)
        )
        try:
            add_res = MYSQL连接.语句执行(add_sql, 交易类型)
        except BaseException as e:
            print('K线图:%s数据添加数据库失败. 原因为:%s' % (币种对, e))
            return
        if add_res <= 0:
            print('K线图:%s%s数据添加数据库失败' % (币种对, K线图类型))


def update_sql(数据, 币种对, K线图类型, MYSQL连接, 交易类型):
    '''修改旧数据
    总获取了n条数据，其中第一条为当前日期，其他均为旧数据，将旧数据更新或者将添加失败的旧数据也更新

    Agrs:
        数据: 接口返回数据
        币种对: 参数二，保存数据
        K线图类型: 参数一，根据值获取对应表名
        MYSQL连接: mysql连接对象
        交易类型: 执行sql语句时区分执行哪个数据库连接, 合约或币币
    '''
    for i in range(1, config.K线图获取数量 - 1):
        select_sql = "select * from %s where  code='%s' and date='%s'" % (
            config.K线图表名[K线图类型],
            币种对.replace('_', '/'),
            time.strftime("%Y-%m-%d %H:%M", time.localtime(数据['data'][i]['id']))
        )
        select_res = MYSQL连接.语句执行(select_sql, 交易类型)
        if select_res == 0:
            content_time = time.localtime(数据['data'][i]['id'])
            update_sql = "insert into %s (%s) value ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                config.K线图表名[K线图类型],
                'code, period, volume, price, opening_price, closing_price, pre_closing_price, highest_price, lowest_price, date_ymd, date, create_time',
                币种对.replace('_', '/'),
                time.strftime("%Y%m%d", content_time),
                round(数据['data'][i]['amount'], 7),  # 成交量
                数据['data'][i]['close'],  # 收盘价
                数据['data'][i]['open'],  # 开盘价
                数据['data'][i]['close'],  # 收盘价
                0,
                数据['data'][i]['high'],  # 最高价
                数据['data'][i]['low'],  # 最低价
                time.strftime("%Y%m%d", content_time),
                time.strftime("%Y-%m-%d %H:%M", content_time),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
        else:
            update_sql = "update %s set volume='%s',price='%s',opening_price='%s',closing_price='%s',highest_price='%s',lowest_price='%s',create_time='%s' where code='%s' and date='%s'" % (
                config.K线图表名[K线图类型],
                数据['data'][i]['amount'],  # 成交量
                数据['data'][i]['close'],  # 收盘价
                数据['data'][i]['open'],  # 开盘价
                数据['data'][i]['close'],  # 收盘价
                数据['data'][i]['high'],  # 最高价
                数据['data'][i]['low'],  # 最低价
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                币种对.replace('_', '/'),
                time.strftime("%Y-%m-%d %H:%M", time.localtime(数据['data'][i]['id']))
            )
        try:
            update_res = MYSQL连接.语句执行(update_sql, 交易类型)
        except BaseException as e:
            print('K线图:%s数据修改数据库失败. 原因为:%s' % (币种对, e))
            return
        if update_res <= 0:
            print('K线图:%s%s数据修改数据库失败' % (币种对, K线图类型))


def worker(币种对, K线图类型, MYSQL连接):
    '''子进程方法
    Agrs:
        币种对: 接口参数二
        K线图类型: 接口参数一
        MYSQL连接: mysql连接对象
    '''
    from config import redis连接

    数据 = get_data(币种对, K线图类型)
    if 数据 == {} or 数据['status'] != 'ok' or 'data' in 数据 is False:
        print('K线图:%s%sk线图数据获取失败' % (币种对, K线图类型))
        return
    # 要分别添加到合约和币币
    if config.合约开关 is True:
        try:
            风控_number = float(redis连接.合约REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        for i in range(0, len(数据['data']) - 1):
            数据['data'][i]['open'] += 风控_number
            数据['data'][i]['close'] += 风控_number
            数据['data'][i]['high'] += 风控_number
            数据['data'][i]['low'] += 风控_number
        add_sql(数据, 币种对, K线图类型, MYSQL连接, '合约')
        update_sql(数据, 币种对, K线图类型, MYSQL连接, '合约')
    if config.币币开关 is True:
        try:
            风控_number = float(redis连接.币币REDIS['%s%s' % (config.风控_KEY, 币种对)].decode()) if (config.使用风控 is True) else 0
        except BaseException:
            风控_number = 0
        for i in range(0, len(数据['data']) - 1):
            数据['data'][i]['open'] += 风控_number
            数据['data'][i]['close'] += 风控_number
            数据['data'][i]['high'] += 风控_number
            数据['data'][i]['low'] += 风控_number
        add_sql(数据, 币种对, K线图类型, MYSQL连接, '币币')
        update_sql(数据, 币种对, K线图类型, MYSQL连接, '币币')


def timekeeping(币种对, 秒数, MYSQL连接):
    '''自定义计时器
    每执行一次休息0.1秒，当当前执行时间与上次执行时间相同时，跳过本轮执行
    Agrs:
        coin_type: 币种类型
    '''
    上次执行时间 = ''
    while True:
        # 防止代码执行时间过长，进行一次新旧时间判断，保证每秒仅执行一次
        当前时间 = time.localtime()
        if 当前时间 == 上次执行时间:
            time.sleep(0.1)
            continue
        上次执行时间 = 当前时间
        # 获取时间
        当前分钟数 = 当前时间.tm_min
        当前秒数 = 当前时间.tm_sec
        # 业务
        if(当前秒数 == 秒数):
            # 一分钟线，每分钟的第一秒执行
            t = threading.Thread(target=worker, args=(币种对, '1min', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 % 5 == 1 and 当前秒数 == 秒数):
            # 五分钟线，每五分钟更新一次
            t = threading.Thread(target=worker, args=(币种对, '5min', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 % 15 == 1 and 当前秒数 == 秒数):
            # 十五分钟线，每十五分钟更新一次
            t = threading.Thread(target=worker, args=(币种对, '15min', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 % 30 == 1 and 当前秒数 == 秒数):
            # 三十分钟线，每三十分钟更新一次
            t = threading.Thread(target=worker, args=(币种对, '30min', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 % 15 == 0 and 当前秒数 == 秒数):
            # 小时线，每十五分钟更新一次
            t = threading.Thread(target=worker, args=(币种对, '60min', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 == 10 and 当前秒数 == 秒数):
            # 4小时线，每小时更新一次
            t = threading.Thread(target=worker, args=(币种对, '4hour', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 == 20 and 当前秒数 == 秒数):
            # 日线，每小时更新一次
            t = threading.Thread(target=worker, args=(币种对, '1day', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 == 30 and 当前秒数 == 秒数):
            # 周线，每小时更新一次
            t = threading.Thread(target=worker, args=(币种对, '1week', MYSQL连接))
            threads.append(t)
            t.start()
        if(当前分钟数 == 40 and 当前秒数 == 秒数):
            # 月线，每小时更新一次
            t = threading.Thread(target=worker, args=(币种对, '1mon', MYSQL连接))
            threads.append(t)
            t.start()
        time.sleep(0.1)
