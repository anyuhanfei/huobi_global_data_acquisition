import time
import copy

import __init__ as init
from config import config
from utils.BaseData import BaseData


class 盘口(BaseData):
    def __init__(self, 币种对, *argv, **kwargv):
        super().__init__(币种对)
        self.index()

    def index(self):
        '''获取数据
        Agrs:
            coin_type: 网址的get参数，传入格式为 NAME/NAME
        '''

        # 处理参数  NAME/NAME -> namename
        币种对格式替换 = init.币种对格式替换(self.币种对, '/', '')
        # 获取返回结果
        盘口URL = init.盘口URL % (币种对格式替换)
        数据 = init.访问URL(盘口URL, 'get')
        if 数据 == {} or 'tick' in 数据 is False:
            print('获取盘口数据:%s盘口数据获取失败' % (self.币种对))
            return None
        # 组合数据
        add_dict = self.combination_data(数据)
        # 储存和发布
        if config.数据存储方式 == 'redis':
            self.add_data_redis(add_dict)
        elif config.数据存储方式 == 'mysql':
            self.add_data_mysql(add_dict)
        else:
            print('获取盘口数据:数据存储类型错误')

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
        add_dict['bids'] = []
        for i in range(0, 20 if len(数据['tick']['bids']) >= 20 else len(数据['tick']['bids'])):
            add_dict['bids'].append({
                'totalSize': 数据['tick']['bids'][i][1],
                'price': round(数据['tick']['bids'][i][0], 2)
            })
        add_dict['asks'] = []
        for i in range(0, 20 if len(数据['tick']['asks']) >= 20 else len(数据['tick']['asks'])):
            add_dict['asks'].append({
                'totalSize': 数据['tick']['asks'][i][1],
                'price': round(数据['tick']['asks'][i][0], 2)
            })
        return add_dict

    def add_data_redis(self, add_data):
        '''将数据存储到redis
        数据转换为json字符串，然后分别添加到通道和存储中
        Agrs:
            add_data: 已整理数据，字典类型
        '''
        if config.合约开关 is True:
            合约add_data = copy.deepcopy(add_data)
            合约add_data['bids'] = []
            合约add_data['asks'] = []
            for bids in add_data['bids']:
                bids['price'] += self.合约风控数值
                合约add_data['bids'].append(bids)
            for asks in add_data['asks']:
                asks['price'] += self.合约风控数值
                合约add_data['asks'].append(asks)
            res_add_data = str(add_data).replace("'", '"').encode()
            self.redis存储('合约', '盘口', res_add_data)
        if config.币币开关 is True:
            币币add_data = copy.deepcopy(add_data)
            币币add_data['bids'] = []
            币币add_data['asks'] = []
            for bids in add_data['bids']:
                bids['price'] += self.币币风控数值
                币币add_data['bids'].append(bids)
            for asks in add_data['asks']:
                asks['price'] += self.币币风控数值
                币币add_data['asks'].append(asks)
            res_add_data = str(add_data).replace("'", '"').encode()
            self.redis存储('币币', '盘口', res_add_data)

    def add_data_mysql(self, add_data):
        pass
