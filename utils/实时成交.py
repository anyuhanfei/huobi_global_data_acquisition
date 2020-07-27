import time

import __init__ as init
from config import config
from utils.BaseData import BaseData


class 实时成交(BaseData):
    def __init__(self, 币种对):
        super().__init__(币种对)
        self.index()

    def index(self):
        '''获取实时成交数据
        '''
        # 处理参数  NAME/NAME -> namename
        币种对格式替换 = init.币种对格式替换(self.币种对, '/', '')
        # 获取返回结果
        实时成交URL = init.实时成交URL % (币种对格式替换)
        数据 = init.访问URL(实时成交URL, 'get')
        if 数据 == {} or 'data' in 数据 is False:
            print('获取实时成交数据:%s实时成交数据获取失败' % (self.币种对))
            return None
        # 组合数据
        add_dict = self.combination_data(数据)
        # 储存和发布
        if config.数据存储方式 == 'redis':
            self.add_data_redis(add_dict)
        elif config.数据存储方式 == 'mysql':
            self.add_data_mysql(add_dict)
        else:
            print('获取实时成交数据:数据存储类型错误')

    def combination_data(self, 数据):
        '''整合数据
        将已知数据整合成指定格式
        Agrs:
            数据: 从接口中返回的数据，字典类型
        Return:
            dict 已整合的数据
        '''
        add_dict = {}
        add_dict['code'] = self.币种对
        add_dict['name'] = self.币种对
        add_dict['date'] = time.strftime('%Y-%m-%d')
        add_dict['time'] = time.strftime('%H:%M')
        add_dict['timestamp'] = int(time.time())
        add_dict['data'] = []

        for i in 数据['data']:
            add_dict['data'].append({
                'dt': i['data'][0]['ts'],
                'dc': i['data'][0]['direction'],
                'amount': i['data'][0]['amount'],
                'price': i['data'][0]['price']
            })
        return add_dict

    def add_data_redis(self, 数据):
        '''将数据存储到redis
        Agrs:
            数据: 已整理数据，字典类型
        '''
        if config.合约开关 is True:
            self.redis存储('合约', '实时成交', '', str(数据).replace("'", '"').encode(), str(数据).encode())
        if config.币币开关 is True:
            self.redis存储('币币', '实时成交', '', str(数据).replace("'", '"').encode(), str(数据).encode())

    def add_data_mysql(self):
        pass
