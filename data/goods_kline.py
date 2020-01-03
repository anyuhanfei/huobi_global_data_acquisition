import time
import threading

import __init__
from config import mysql_conn

# 周期对应的表名
table_name = {
    '1min': 'goods_kline_min1_info',
    '5min': 'goods_kline_min5_info',
    '15min': 'goods_kline_min15_info',
    '30min': 'goods_kline_min30_info',
    '60min': 'goods_kline_min60_info',
    '1day': 'goods_kline_day1_info',
    '1week': 'goods_kline_week_info',
    '1mon': 'goods_kline_month_info'
}

# 多线程队列
threads = []


def get_data(coin_type, period):
    '''访问接口，获取返回数据
    Agrs:
        coin_type: 接口参数二，传来格式为 NAME_NAME，需修改为 namename
        period: 接口参数一，k线图时间类型
    return:
        dict 接口返回的无修改数据
    '''
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '_', '')
    get_data_url = __init__.goods_kline_url % (period, coin_type_dispose)
    get_data_content = __init__.get_url(get_data_url, 'get')
    return get_data_content


def add_sql(content, coin_type, period):
    '''添加数据
    Agrs:
        content: 接口返回数据
        coin_type: 参数二，保存数据
        period: 参数一，根据值获取对应表名
    '''
    content_time = time.localtime(content['data'][0]['id'])
    add_sql = "insert into %s (code, period, volume, price, opening_price, closing_price, pre_closing_price, highest_price, lowest_price, date_ymd, date, create_time) value ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        table_name[period],
        coin_type,
        time.strftime("%Y%m%d", content_time),
        content['data'][0]['amount'],
        content['data'][0]['close'],
        content['data'][0]['open'],
        content['data'][0]['close'],
        0,
        content['data'][0]['high'],
        content['data'][0]['low'],
        time.strftime("%Y%m%d", content_time),
        time.strftime("%Y-%m-%d %H:%M", content_time),
        time.strftime("%Y-%m-%d %H:%M:%S", content_time)
    )
    try:
        mysql_conn.MYSQL.ping(reconnect=True)
        add_res = mysql_conn.CURSOR.execute(add_sql)
        mysql_conn.MYSQL.commit()
    except BaseException as e:
        __init__.add_log('kline', coin_type, e, 1)
        return
    if add_res > 0:
        __init__.add_log('kline', coin_type, '数据添加数据库完成', 1)
    else:
        __init__.add_log('kline', coin_type, '数据添加数据库失败', 1)


def worker(coin_type, period):
    '''子进程方法
    Agrs:
        coin_type: 接口参数二
        period: 接口参数一
    '''
    content = get_data(coin_type, period)
    if content == {}:
        __init__.add_log('kline', coin_type, 'k线图数据获取失败', 1)
        return
    add_sql(content, coin_type, period)


def timekeeping(coin_type):
    '''自定义计时器
    每执行一次休息0.1秒，当当前执行时间与上次执行时间相同时，跳过本轮执行
    Agrs:
        coin_type: 币种类型
    '''
    old_time = ''
    while True:
        # 防止代码执行时间过长，进行一次新旧时间判断，保证每秒仅执行一次
        new_time = time.localtime()
        if new_time == old_time:
            time.sleep(0.1)
            continue
        old_time = new_time
        # 获取时间
        new_hour = new_time.tm_hour
        new_minute = new_time.tm_min
        new_second = new_time.tm_sec
        new_day = '%s%s%s' % (new_hour, new_minute, new_second)
        new_week = new_time.tm_wday
        # 业务
        if(new_second == 1):
            # 一分钟线，每分钟的第一秒执行
            __init__.add_log('kline', coin_type, '一分钟线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '1min', ))
            threads.append(t)
            t.start()
        if(new_minute % 5 == 1 and new_second == 1):
            # 五分钟线，第六分钟的第一秒执行
            __init__.add_log('kline', coin_type, '五分钟线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '5min', ))
            threads.append(t)
            t.start()
        if(new_minute % 15 == 1 and new_second == 1):
            # 十五分钟线，第十六分钟的第一秒执行
            __init__.add_log('kline', coin_type, '十五分钟线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '15min', ))
            threads.append(t)
            t.start()
        if(new_minute % 30 == 1 and new_second == 1):
            # 三十分钟线，第三十一分钟的第一秒执行
            __init__.add_log('kline', coin_type, '三十分钟线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '30min', ))
            threads.append(t)
            t.start()
        if(new_minute % 15 == 0 and new_second == 1):
            # 小时线，每十五分钟更新一次
            __init__.add_log('kline', coin_type, '小时线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '60min', ))
            threads.append(t)
            t.start()
        if(new_minute == 0 and new_second == 1):
            # 日线，每小时更新一次
            __init__.add_log('kline', coin_type, '日线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '1day', ))
            threads.append(t)
            t.start()
        if(new_day == '001'):
            # 周线，每天更新一次
            __init__.add_log('kline', coin_type, '周线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '1week', ))
            threads.append(t)
            t.start()
        if(new_day == '001' and new_week == 0):
            # 月线，每周更新一次
            __init__.add_log('kline', coin_type, '月线：', 0)
            t = threading.Thread(target=worker, args=(coin_type, '1mon', ))
            threads.append(t)
            t.start()
        time.sleep(0.1)
