# src/data_ingestion/transformers/stock_transformer.py
"""
股票数据转换器
"""

import pandas as pd
from src.core.logger import logger


class StockTransformer:
    """
    股票数据转换器
    """

    @staticmethod
    def transform_stock_daily_data(stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        转换股票日线数据
        """
        # 检查输入是否为 DataFrame
        if not isinstance(stock_data, pd.DataFrame):
            logger.error("Input data is not a pandas DataFrame.")
            raise ValueError("Input data must be a pandas DataFrame.")

        # 检查 DataFrame 是否为空
        if stock_data.empty:
            logger.warning("DataFrame is empty, no transformation needed.")
            return stock_data

        # 检查是否缺少必要的列
        required_columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'outstanding_share',
                            'turnover']
        if not all(col in stock_data.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in stock_data.columns]
            logger.error(f"Missing required columns: {missing_columns}")
            raise ValueError(f"DataFrame missing required columns: {missing_columns}")

        try:
            # 转换 'date' 列为日期类型
            stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date

            # 确保数值列是 float 类型
            numeric_columns = ['open', 'close', 'high', 'low', 'volume', 'amount', 'outstanding_share', 'turnover']
            for col in numeric_columns:
                stock_data[col] = pd.to_numeric(stock_data[col], errors='coerce').fillna(0.0)

            # 打印转换后的数据的前几行，用于调试
            logger.debug(f"Transformed data sample:\n{stock_data.head()}")

            return stock_data

        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            raise