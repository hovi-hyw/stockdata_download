# src/core/exceptions.py
"""
自定义异常模块
"""

class DataFetchError(Exception):
    """
    数据获取失败异常
    """
    pass


class DataSaveError(Exception):
    """
    数据保存失败异常
    """
    pass