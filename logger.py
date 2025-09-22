"""
模块名：日志记录器-logger.py
模块说明：
- 日志记录器模块主要进行程序运行日志的记录
- 日志记录器包含控制台处理器和文件处理器，文件处理器进行日志轮转，单个文件最大 10MB ，最多保留 1 个备份
"""
from logging.handlers import RotatingFileHandler
import logging


LOG_PATH = 'run.log'   # 日志文件路径


# 创建日志记录器
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)


# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter(
        f"[%(levelname)s][%(asctime)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)

# 创建文件处理器
file_handler = RotatingFileHandler(
    filename=LOG_PATH,
    encoding='utf-8',
    maxBytes=10*1024*1024,  # 单日志最大10MB
    backupCount=1  # 只留1个备份文件
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)

# 将处理器添加到 logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 禁止根记录器输出日志
logging.getLogger().setLevel(logging.CRITICAL)


if __name__ == '__main__':
    print('此模块不可单独运行！！')
