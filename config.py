"""
模块名：配置文件-config.py
模块说明:
- 该模块主要保存程序运行时所需的各种全局变量或信息记录，同时负责从静态配置文件 config.json 中加载配置信息
"""
import json


# 加载配置文件 config.json 中的信息
def load():
    """
    - 加载 config.json 文件中的信息，若无文件则报错
    - 无传入参数，有返回值，无日志记录
    Returns:
        返回读取到的信息
    """
    try:
        with open('config.json', 'r') as file:
            cfg = json.load(file)
    except FileNotFoundError:
        pass
    return cfg


Author = "Le_0x7E"

Config = load()   # 从config.json文件中加载的信息


if __name__ == '__main__':
    print('此模块不可单独运行！！')
