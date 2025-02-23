# src/data_ingestion/transformers/index_transformer.py
"""
指数数据转换器
"""

import pandas as pd
from src.core.logger import logger
from src.core.config import config


class BaseTransformer:
    """
    数据转换器的抽象基类
    """
    @staticmethod
    def _validate_dataframe(data: pd.DataFrame, required_columns: list):
        """
        验证 DataFrame 是否有效，包括类型检查和缺失值处理
        """
        if not isinstance(data, pd.DataFrame):
            logger.error("Input data is not a pandas DataFrame.")
            raise ValueError("Input data must be a pandas DataFrame.")

        if data.empty:
            logger.warning("DataFrame is empty, no transformation needed.")
            return False

        if not all(col in data.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in data.columns]
            logger.error(f"Missing required columns: {missing_columns}")
            raise ValueError(f"DataFrame missing required columns: {missing_columns}")
        return True


class IndexTransformer:
    """
    指数数据转换器
    """

    @staticmethod
    def transform_index_daily_data(index_data: pd.DataFrame) -> pd.DataFrame:
        """
        转换指数日线数据
        """
        required_columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']

        if config.TRANSFORMER_VALIDATE_DATA:  # 从 config 中读取是否开启数据验证
            if not BaseTransformer._validate_dataframe(index_data, required_columns):
                return index_data  # 如果 DataFrame 无效，则直接返回

        try:
            # 转换 '日期' 列为日期类型
            index_data['日期'] = pd.to_datetime(index_data['日期']).dt.date

            # 确保数值列是 float 类型
            numeric_columns = ['开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
            for col in numeric_columns:
                index_data[col] = pd.to_numeric(index_data[col], errors='coerce').fillna(0.0)

            # 打印转换后的数据的前几行，用于调试
            logger.debug(f"Transformed data sample:\n{index_data.head()}")

            return index_data

        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            raise