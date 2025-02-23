# src/core/logger.py
"""
日志模块
"""

import logging
import os
from datetime import datetime

from src.core.config import config

# 确保日志目录存在
if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)

# 获取今天的日期
today = datetime.now().strftime("%Y-%m-%d")

# 构建今天的日志文件名
log_file = os.path.join(config.LOG_DIR, f"stockdata_download_{today}.log")

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

# 创建文件处理器，按日期分割日志
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(config.LOG_LEVEL)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(config.LOG_LEVEL)

# 创建格式化器
formatter = logging.Formatter(config.LOG_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)