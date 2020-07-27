import time
import copy

import __init__ as init
from config import config
from utils.BaseData import BaseData


class 深度图(BaseData):
    def __init__(self, 币种对):
        super().__init__(币种对)
        self.index()

    def index(self):
        '''获取深度图数据
        '''
        # 处理参数  NAME/NAME -> namename
        币种对格式替换 = init.币种对格式替换(self.币种对, '/', '')
        # 获取返回结果
        深度图URL = init.深度图URL % (币种对格式替换)
        数据 = init.访问URL(深度图URL, 'get')
        if 数据 == {} or 'tick' in 数据 is False:
            print('获取深度图数据:%s深度图数据获取失败' % (self.币种对))
            return None
        # 组合数据
        add_dict = self.combination_data(数据)
        # 储存和发布
        if config.数据存储方式 == 'redis':
            self.add_data_redis(add_dict)
        elif config.数据存储方式 == 'mysql':
            self.add_data_mysql(add_dict)
        else:
            print('获取深度图数据:数据存储类型错误')

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
        bids = 0
        for i in range(0, 200 if len(数据['tick']['bids']) >= 200 else len(数据['tick']['bids'])):
            bids += round(数据['tick']['bids'][i][1], 2)
            add_dict['bids'].append({
                'totalSize': bids,
                'price': round(数据['tick']['bids'][i][0], 5)
            })
        add_dict['asks'] = []
        asks = 0
        for i in range(0, 200 if len(数据['tick']['asks']) >= 200 else len(数据['tick']['asks'])):
            asks += round(数据['tick']['asks'][i][1], 2)
            add_dict['asks'].append({
                'totalSize': asks,
                'price': round(数据['tick']['asks'][i][0], 5)
            })
        return add_dict

    def add_data_redis(self, add_data):
        '''将数据存储到redis
        数据转换为json字符串，然后分别添加到通道和存储中
        Agrs:
            add_dict: 已整理数据，字典类型
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
            self.redis存储('合约', '深度图', res_add_data)
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
            self.redis存储('币币', '深度图', res_add_data)

    def add_data_mysql(self, add_data):
        pass
