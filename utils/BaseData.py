'''
获取数据的基类
'''
from config import config
from config import redis连接


class BaseData:
    合约风控数值 = 0
    币币风控数值 = 0

    合约CNY汇率 = 1
    币币CNY汇率 = 1

    币种对 = ''

    def __init__(self, 币种对, *argv, **kwargv):
        '''
        '''
        self.币种对 = 币种对
        self.设置风控()
        self.CNY汇率读取()

    def 设置风控(self):
        try:
            self.合约风控数值 = float(redis连接.合约REDIS['%s%s' % (config.风控_KEY, self.币种对)].decode()) if (config.使用风控 is True and config.合约开关 is True) else 0
        except BaseException:
            pass
        try:
            self.币币风控数值 = float(redis连接.币币REDIS['%s%s' % (config.风控_KEY, self.币种对)].decode()) if (config.使用风控 is True and config.币币开关 is True) else 0
        except BaseException:
            pass

    def CNY汇率读取(self):
        coin = self.币种对.split('/')
        if config.合约开关 is True:
            if coin[1] == 'USDT':
                self.合约CNY汇率 = float(redis连接.合约REDIS[config.USDT2CNY].decode())
            elif coin[1] == 'BTC':
                self.合约CNY汇率 = float(redis连接.合约REDIS[config.BTC2CNY].decode())
            elif coin[1] == 'ETH':
                self.合约CNY汇率 = float(redis连接.合约REDIS[config.USDT2CNY].decode()) * float(redis连接.合约REDIS['exchange:vb:ticker:newprice:ETH/USDT'].decode())
            else:
                print('合约CNY汇率读取失败')
                return
        if config.币币开关 is True:
            if coin[1] == 'USDT':
                self.币币CNY汇率 = float(redis连接.币币REDIS[config.USDT2CNY].decode())
            elif coin[1] == 'BTC':
                self.币币CNY汇率 = float(redis连接.币币REDIS[config.BTC2CNY].decode())
            elif coin[1] == 'ETH':
                self.币币CNY汇率 = float(redis连接.币币REDIS[config.USDT2CNY].decode()) * float(redis连接.币币REDIS['exchange:vb:ticker:newprice:ETH/USDT'].decode())
            else:
                print('币币CNY汇率读取失败')
                return

    def redis存储(self, 交易方式, 数据类型, 数据='', 推送数据='', 存储数据=''):
        '''将已整理好的数据存储到 redis 中
        根据配置文件配置, 最大将数据存储两份, 一份更新存储, 一份添加至推送中
        Args:
            交易方式: '合约' / '币币'
            数据类型: '盘口' / '深度图' / '实时成交' / '实时行情' / '最新价格'
            数据: 已整理好的数据
            推送数据: 要推送的数据, 当推送数据和存储数据不同时使用, 若要使用请将 `数据` 参数传空(任何对应布尔值为False的类型皆可), 下同
            存储数据: 存储起来的数据
        '''
        if ['合约', '币币'].count(交易方式) <= 0:
            print('交易方式传入错误')
            return
        if ['盘口', '深度图', '实时成交', '实时行情', '最新价格'].count(数据类型) <= 0:
            print('数据类型传入错误')
            return
        temp_dict = {
            '合约': {
                'publish': {
                    '盘口': config.合约_publish_盘口,
                    '深度图': config.合约_publish_深度图,
                    '实时成交': config.合约_publish_实时成交,
                    '实时行情': config.合约_publish_实时行情,
                    '最新价格': config.合约_publish_最新价格
                },
                'set': {
                    '盘口': config.合约_set_盘口 % (self.币种对),
                    '深度图': config.合约_set_深度图 % (self.币种对),
                    '实时成交': config.合约_set_实时成交 % (self.币种对),
                    '实时行情': config.合约_set_实时行情 % (self.币种对),
                    '最新价格': config.合约_set_最新价格 % (self.币种对),
                }
            },
            '币币': {
                'publish': {
                    '盘口': config.币币_publish_盘口,
                    '深度图': config.币币_publish_深度图,
                    '实时成交': config.币币_publish_实时成交,
                    '实时行情': config.币币_publish_实时行情,
                    '最新价格': config.币币_publish_最新价格
                },
                'set': {
                    '盘口': config.币币_set_盘口 % (self.币种对),
                    '深度图': config.币币_set_深度图 % (self.币种对),
                    '实时成交': config.币币_set_实时成交 % (self.币种对),
                    '实时行情': config.币币_set_实时行情 % (self.币种对),
                    '最新价格': config.币币_set_最新价格 % (self.币种对),
                }
            },
        }
        连接obj = redis连接.合约REDIS if 交易方式 == '合约' else redis连接.币币REDIS
        连接obj.publish(temp_dict[交易方式]['publish'][数据类型], 推送数据 if (bool(数据) is False) else 数据)
        连接obj.set(temp_dict[交易方式]['set'][数据类型], 存储数据 if (bool(数据) is False) else 数据)
