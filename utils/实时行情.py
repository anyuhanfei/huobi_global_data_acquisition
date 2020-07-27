import time

import __init__ as init
from config import config
from utils.BaseData import BaseData


class 实时行情(BaseData):
    def __init__(self, 币种对):
        super().__init__(币种对)
        self.index()

    def index(self):
        '''实时行情获取
        Agrs:
            币种对: 网址的get参数，传入格式为 NAME/NAME
        '''
        # 处理参数  NAME/NAME -> namename
        币种对格式替换 = init.币种对格式替换(self.币种对, '/', '')
        # 获取返回结果
        实时行情URL = init.实时行情URL % (币种对格式替换)
        数据 = init.访问URL(实时行情URL, 'get')
        if 数据 == {} or 'tick' in 数据 is False:
            print('实时行情获取:%s实时行情获取失败' % (self.币种对))
            return None
        # 储存和发布
        if config.数据存储方式 == 'redis':
            self.get_data_redis(数据)
        elif config.数据存储方式 == 'mysql':
            self.get_data_mysql(数据)
        else:
            print('实时行情获取:数据存储类型错误')

    def combination_data(self, 数据, 风控数值, CNY汇率):
        '''整合数据
        将已知数据整合成指定格式
        Agrs:
            币种对: 币种
            风控数值: 风控设置的值
        Return:
            dict 已整合的数据
        '''
        add_dict = {
            'code': self.币种对,
            'name': self.币种对,
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M'),
            'timestamp': int(time.time()),
            'price': 数据['tick']['close'] + 风控数值,
            'cnyPrice': (数据['tick']['close'] + 风控数值) * CNY汇率,  # 这里是要获取usdt的价格
            'open': 数据['tick']['open'] + 风控数值,
            'close': 数据['tick']['close'] + 风控数值,
            'high': 数据['tick']['high'] + 风控数值,
            'low': 数据['tick']['low'] + 风控数值,
            'volume': 数据['tick']['amount'],
            'change': 数据['tick']['close'] - 数据['tick']['open'],
            'changeRate': str(round((数据['tick']['close'] - 数据['tick']['open']) / 数据['tick']['open'] * 100, 2)) + '%',
            'buy': 数据['tick']['bid'][0],
            'sell': 数据['tick']['ask'][0]
        }
        return add_dict

    def get_data_redis(self, 数据):
        '''将数据存储到redis
        获取到usdt兑换cny的比例，然后组合数据，将组合完成的数据加入到redis中
        Agrs:
            币种对: 货币类型
            数据: 未整理数据，字典类型
        '''
        if config.合约开关 is True:
            add_dict = self.combination_data(数据, self.合约风控数值, self.合约CNY汇率)
            self.redis存储('合约', '实时行情', '', str(add_dict).replace("'", '"').encode(), str(add_dict).encode())
        if config.币币开关 is True:
            add_dict = self.combination_data(数据, self.合约风控数值, self.币币CNY汇率)
            self.redis存储('币币', '实时行情', '', str(add_dict).replace("'", '"').encode(), str(add_dict).encode())

    def get_data_mysql(self):
        '''实时行情获取(mysql)'''
        pass
