import pymysql
from DBUtils.PooledDB import PooledDB

from config import config


class MYSQL连接:
    '''mysql连接自定义类'''

    def __init__(self):
        if config.合约开关 is True:
            self.合约POOL = PooledDB(
                creator=pymysql,
                maxconnections=0,
                mincached=10,
                maxcached=5,
                maxshared=0,
                blocking=True,
                maxusage=None,
                setsession=[],
                ping=0,
                host=config.合约_MYSQL_HOST,
                port=config.合约_MYSQL_PORT,
                user=config.合约_MYSQL_USER,
                password=config.合约_MYSQL_PASSWORD,
                database=config.合约_MYSQL_DBNAME,
                charset=config.合约_MYSQL_CHARSET
            )
        if config.币币开关 is True:
            self.币币POOL = PooledDB(
                creator=pymysql,
                maxconnections=0,
                mincached=10,
                maxcached=5,
                maxshared=0,
                blocking=True,
                maxusage=None,
                setsession=[],
                ping=0,
                host=config.币币_MYSQL_HOST,
                port=config.币币_MYSQL_PORT,
                user=config.币币_MYSQL_USER,
                password=config.币币_MYSQL_PASSWORD,
                database=config.币币_MYSQL_DBNAME,
                charset=config.币币_MYSQL_CHARSET
            )

    def 语句执行(self, sql, 连接类型):
        if 连接类型 == '合约':
            conn = self.合约POOL.connection()
        elif 连接类型 == '币币':
            conn = self.币币POOL.connection()
        else:
            return False
        cursor = conn.cursor()
        result = cursor.execute(sql)
        conn.commit()
        conn.close()
        return result
