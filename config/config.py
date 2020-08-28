"""
系统全局配置
    盘口, 深度图, 行情, 实时行情统称为推送;
"""
import copy


'''数据获取间隔时间(s)'''
推送间隔时间 = 1

'''币种对'''
USDT币种对 = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'BCH/USDT', 'EOS/USDT']  # USDT相关币种对
ETH币种对 = ['EOS/ETH', 'ADA/ETH', 'OMG/ETH']  # ETH相关币种对
BTC币种对 = ['LTC/BTC', 'BCH/BTC', 'ETH/BTC', 'EOS/BTC', 'XRP/BTC', 'ETC/BTC']  # BTC相关币种对

币种对 = USDT币种对

'''日志记录'''
日志开关 = True

'''使用存储方式 redis or mysql'''
数据存储方式 = 'redis'
K线图存储方式 = 'mysql'

'''交易方式开关'''
合约开关 = True
币币开关 = False

'''合约方式的redis和mysql配置'''
合约_REDIS_HOST = '127.0.0.1'
合约_REDIS_PORT = 6379
合约_REDIS_AUTH = ''
合约_REDIS_PASSWROD = ''

合约_MYSQL_HOST = '127.0.0.1'
合约_MYSQL_PORT = 3306
合约_MYSQL_USER = 'root'
合约_MYSQL_PASSWORD = 'root'
合约_MYSQL_DBNAME = 'k'
合约_MYSQL_CHARSET = 'utf8'

'''币币方式的redis和mysql配置'''
币币_REDIS_HOST = '127.0.0.1'
币币_REDIS_PORT = 6379
币币_REDIS_AUTH = ''
币币_REDIS_PASSWROD = ''

币币_MYSQL_HOST = '127.0.0.1'
币币_MYSQL_PORT = 3306
币币_MYSQL_USER = 'root'
币币_MYSQL_PASSWORD = 'root'
币币_MYSQL_DBNAME = 'k'
币币_MYSQL_CHARSET = 'utf8'

'''合约方式的redis键设置'''
合约_publish_最新价格 = ""
合约_publish_实时行情 = "contract:vb:ticker:chan:mobei"
合约_publish_深度图 = "contract:vb:depth:pct:chan:mobei"
合约_publish_盘口 = "contract:vb:depth:chan:mobei"
合约_publish_实时成交 = "contract:vb:trader:chan:mobei"

合约_set_最新价格 = "contract:vb:ticker:newprice:%s"
合约_set_实时行情 = "contract:vb:ticker:newitem:%s"
合约_set_深度图 = "contract:vb:depth:pct:newitem:%s"
合约_set_盘口 = "contract:vb:depth:newitem:%s"
合约_set_实时成交 = "contract:vb:trader:newitem:%s"

'''币币方式的redis键值设置'''
币币_publish_最新价格 = ""
币币_publish_实时行情 = "exchange:vb:ticker:chan:mobei"
币币_publish_深度图 = "exchange:vb:depth:pct:chan:mobei"
币币_publish_盘口 = "exchange:vb:depth:chan:mobei"
币币_publish_实时成交 = "exchange:vb:trader:chan:mobei"

币币_set_最新价格 = "exchange:vb:ticker:newprice:%s"
币币_set_实时行情 = "exchange:vb:ticker:newitem:%s"
币币_set_深度图 = "exchange:vb:depth:pct:newitem:%s"
币币_set_盘口 = "exchange:vb:depth:newitem:%s"
币币_set_实时成交 = "exchange:vb:trader:newitem:%s"

'''其他redis键值'''
USDT2CNY = 'vb:indexTickerAll:usd2cny'
BTC2CNY = 'vb:indexTickerAll:btc2cny'

'''风控'''
使用风控 = True
风控_KEY = 'contract:vb:risk:management:'  # 例: vb:risk:management:GOLD/USDT

# 周期对应的表名
K线图表名 = {
    '1min': 'goods_kline_min1_info',
    '5min': 'goods_kline_min5_info',
    '15min': 'goods_kline_min15_info',
    '30min': 'goods_kline_min30_info',
    '60min': 'goods_kline_min60_info',
    '4hour': 'goods_kline_hour4_info',
    '1day': 'goods_kline_day1_info',
    '1week': 'goods_kline_week_info',
    '1mon': 'goods_kline_month_info'
}

'''其他设置'''
K线图获取数量 = 7

'''自动设置'''
推送币种对 = copy.copy(币种对)
K线图币种对 = copy.copy(币种对)
for i in range(0, len(币种对)):
    K线图币种对[i] = 币种对[i].replace('/', '_')
