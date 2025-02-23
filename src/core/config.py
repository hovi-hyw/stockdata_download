# src/core/config.py
"""
项目配置模块
"""

import os
from dotenv import load_dotenv

# 获取项目根目录的绝对路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# 加载环境变量
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


class Config:
    """
    项目配置类
    """
    # 基础路径配置
    PROJECT_ROOT = PROJECT_ROOT

    # 其他路径配置(使用绝对路径)
    CACHE_PATH = os.path.join(PROJECT_ROOT, os.getenv("CACHE_PATH", "cache"))
    LOG_FILE = os.path.join(PROJECT_ROOT, os.getenv("LOG_FILE", "logs/stockdata_download.log"))

    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL")

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # AkShare API 配置 (如果需要)
    # AKSHARE_API_KEY = os.getenv("AKSHARE_API_KEY", "")

    # 列表更新频率
    MAX_CSV_AGE_DAYS = int(os.getenv("MAX_CSV_AGE_DAYS", 100))

    # 数据更新频率（天）
    # DATA_UPDATE_INTERVAL = int(os.getenv("DATA_UPDATE_INTERVAL", 100))

    # stock_zh_a_daily\index_zh_a_hist重试次数和间隔
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))
    GET_TIMEOUT = int(os.getenv("GET_TIMEOUT", 10))

    # 并行线程数
    MAX_THREADS = int(os.getenv("MAX_THREADS", 12))

    # 批量插入大小
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

    # API 重试次数
    API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", 3))

    # API 重试间隔
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", 1))

    # 数据缓存目录
    DATA_CACHE_DIR = os.getenv("DATA_CACHE_DIR", "data_cache")


# 实例化配置对象
config = Config()