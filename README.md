# huobi_global_data_acquisition
![py37]py37

通过火币网提供的公共 `API` 接口获取数据并进行一定的整理, 然后存储到数据库中.

开发环境与已使用的生产环境均为 `python3.7` 版本.

## 功能具体介绍

`K线图`, `盘口`, `深度图`, `实时成交`, `实时行情`, `最新价格`均是通过火币网提供的公共 `API` 接口获取到的数据, `CNY汇率`数据是通过火币网的一个非公开 `API` 接口获取到的数据(这里非公开意思仅仅表示在火币网的 `API` 接口文件中没有说明).

`K线图`与`其他数据`的获取分成了两个执行程序, 原因是`K线图`每个类型的线只有到一定的时间获取到的数据才有价值, 不需要每秒都获取数据. 获取`其他数据`所追求的就是更新速度越快越好.

有`合约`, `币币交易`两种模式, 二者执行所获取的数据相同, 存储数据时单独存储, 风控设置也是单独设置.

## 需安装第三方库
- requests
- pymysql
- DBUtils
- redis

## 如何使用

#### window
手动安装第三方库后, 可在项目根目录下分别运行 `data_index.py` 和 `kline_index.py`.

生产环境下, 可直接开启两个 `cmd` 命令行分别执行两个入口文件, `cmd` 命令行保持开启状态即可.

#### linux
进入项目根目录下的 `shell` 目录, 查看两个 `sh` 文件是否有执行权限(下载后应该是没有执行权限的), 需要给这两个 `sh` 文件给予执行权限.

在服务器上初次下载需要先执行 `install_library.sh` 文件, 安装 `python3`, `screen` 以及项目运行所需的 `python` 第三方库.

然后在项目根目录下执行 `./shell/open_service.sh`, 在 `linux` 中是使用 `screen` 服务来实现持久执行的.

注: `./shell/open_service.sh` 还有重启效果.

## 文件树状图

- `config` 配置文件目录
    - `config.py` 配置文件, 所有可变动变量均在这里修改
    - `mysql连接.py` mysql连接自定义方法
    - `redis连接.py` redis连接自定义方法
- `data` 数据存放目录
    - `kline` K线图的 mysql 数据库
- `log` 日志目录
- `shell` sh执行文件目录
    - `install_library.sh` 环境, 服务, python 第三方库一键安装脚本
    - `open_service.sh` 执行程序脚本
- `utils` 获取数据
- `__init__.py` 不需要修改的全局变量与全局方法
- `data_index.py` 数据获取执行文件
- `kline_index.py` K线图获取执行文件

## 主要功能

- 获取深度图数据
- 获取盘口数据
- 获取最新价格
- 获取实时行情
- 获取USDT汇率
- 获取各个时段的K线图
