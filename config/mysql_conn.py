import pymysql
from DBUtils.PooledDB import PooledDB

import __init__


class sqlLink:
    '''mysql连接自定义类'''

    POOL = PooledDB(
        creator=pymysql,   # 使用连接数据库的模块
        maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=10,  # 初始化时，连接池中至少创建的空闲的连接，0表示不创建
        maxcached=5,  # 连接池中最多闲置的连接，0和None不限制
        maxshared=0,
        # 连接池中最多共享的连接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有连接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个连接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用，如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host=__init__.MYSQL_HOST,
        port=__init__.MYSQL_PORT,
        user=__init__.MYSQL_USER,
        password=__init__.MYSQL_PASSWORD,
        database=__init__.MYSQL_DBNAME,
        charset=__init__.MYSQL_CHARSET
    )

    def __init__(self):
        pass
        # try:
        #     self.MYSQL = pymysql.connect(
        #         host=__init__.MYSQL_HOST,
        #         port=__init__.MYSQL_PORT,
        #         user=__init__.MYSQL_USER,
        #         password=__init__.MYSQL_PASSWORD,
        #         db=__init__.MYSQL_DBNAME,
        #         charset=__init__.MYSQL_CHARSET
        #     )
        #     self.CURSOR = self.MYSQL.cursor()
        # except BaseException:
        #     print('mysql连接失败')

    def my_execute(self, sql):
        # 检测当前正在运行连接数的是否小于最大连接数，如果不小于则：等待或报raise TooManyConnections异常
        # 否则
        # 则优先去初始化时创建的连接中获取连接 SteadyDBConnection。
        # 然后将SteadyDBConnection对象封装到PooledDedicatedDBConnection中并返回。
        # 如果最开始创建的连接没有连接，则去创建一个SteadyDBConnection对象，再封装到PooledDedicatedDBConnection中并返回。
        # 一旦关闭连接后，连接就返回到连接池让后续线程继续使用。
        conn = self.POOL.connection()
        cursor = conn.cursor()
        result = cursor.execute(sql)
        conn.commit()
        conn.close()
        return result
