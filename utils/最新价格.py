import __init__ as init
from config import config
from utils.BaseData import BaseData


class 最新价格(BaseData):
    def __init__(self, 币种对):
        super().__init__(币种对)
        self.index()

    def index(self):
        '''获取最新价格
        Agrs:
            币种对: 网址的get参数，传入格式为 NAME/NAME
        '''
        # 处理参数  NAME/NAME -> namename
        币种对格式替换 = init.币种对格式替换(self.币种对, '/', '')
        # 获取返回结果
        最新价格URL = init.最新价格URL % (币种对格式替换)
        数据 = init.访问URL(最新价格URL, 'get')
        if 数据 == {} or 'tick' in 数据 is False:
            print('获取最新价格:%s最新价格获取失败' % (self.币种对))
            return None
        # 储存和发布
        if config.数据存储方式 == 'redis':
            self.add_data_redis(数据)
        elif config.推送存储方式 == 'mysql':
            self.add_data_mysql(数据)
        else:
            print('获取最新价格:数据存储类型错误')

    def add_data_redis(self, data):
        '''将数据存储到redis
        Agrs:
            data: 已整理数据，字典类型
        '''
        if config.合约开关 is True:
            self.redis存储('合约', '最新价格', data['tick']['close'] + self.合约风控数值)
        if config.币币开关 is True:
            self.redis存储('币币', '最新价格', data['tick']['close'] + self.币币风控数值)

    def add_data_mysql(self, data):
        pass
