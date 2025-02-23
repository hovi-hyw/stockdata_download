# src/core/logger.py
"""
日志配置模块
"""

import logging
from src.core.config import config

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

# 创建控制台处理程序
ch = logging.StreamHandler()
ch.setLevel(config.LOG_LEVEL)

# 创建文件处理程序
fh = logging.FileHandler(config.LOG_FILE)
fh.setLevel(config.LOG_LEVEL)

# 创建格式化器
formatter = logging.Formatter(config.LOG_FORMAT)

# 将格式化器添加到处理程序
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# 将处理程序添加到记录器
logger.addHandler(ch)
logger.addHandler(fh)