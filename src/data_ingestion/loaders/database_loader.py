# src/data_ingestion/loaders/database_loader.py
"""
数据库加载器
"""

from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database.models.stock import StockDailyData
from src.database.models.index import IndexDailyData
from src.database.models.concept import ConceptBoardData
from src.core.logger import logger
from src.core.exceptions import DataSaveError
from src.core.config import config
import pandas as pd


class DatabaseLoader:
    """
    数据库加载器
    """

    @staticmethod
    def load_stock_daily_data(stock_data: pd.DataFrame, symbol: str):
        """
        加载股票日线数据到数据库
        """
        try:
            logger.info(f"Loading daily data for stock {symbol} to database...")
            db: Session = next(get_db())
            # updated_count = 0
            # inserted_count = 0

            # 准备插入的数据
            data_to_insert = []
            for _, row in stock_data.iterrows():
                row_date_str = row["date"]
                row_date = pd.to_datetime(row_date_str, errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row_date_str}")
                    continue

                data_to_insert.append(
                    StockDailyData(
                        symbol=symbol,
                        date=row_date,
                        open=row["open"],
                        close=row["close"],
                        high=row["high"],
                        low=row["low"],
                        volume=row["volume"],
                        amount=row["amount"],
                        outstanding_share=row["outstanding_share"],
                        turnover=row["turnover"]
                    )
                )
            # 批量插入数据
            db.bulk_save_objects(data_to_insert)
            db.commit()
            logger.info(f"Inserted {len(data_to_insert)} new records for stock {symbol}.")

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save daily data for stock {symbol} to database: {e}")
            raise DataSaveError(f"Failed to save daily data for stock {symbol} to database: {e}")

    @staticmethod
    def load_index_daily_data(index_data: pd.DataFrame, symbol: str, index_name: str):
        """
        加载指数日线数据到数据库
        """
        try:
            logger.info(f"Loading daily data for index {symbol}({index_name}) to database...")
            db: Session = next(get_db())

            data_to_insert = []
            for _, row in index_data.iterrows():
                row_date_str = row["日期"]
                row_date = pd.to_datetime(row_date_str, errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row_date_str}")
                    continue

                data_to_insert.append(
                    IndexDailyData(
                        symbol=symbol,
                        name=index_name,
                        date=row_date,
                        open=row["开盘"],
                        close=row["收盘"],
                        high=row["最高"],
                        low=row["最低"],
                        volume=row["成交量"],
                        amount=row["成交额"] / 10000.0,
                        amplitude=row["振幅"],
                        change_rate=row["涨跌幅"],
                        change_amount=row["涨跌额"],
                        turnover_rate=row["换手率"]
                    )
                )

            db.bulk_save_objects(data_to_insert)
            db.commit()
            logger.info(f"Inserted {len(data_to_insert)} new records for index {symbol}.")

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save daily data for index {symbol} to database: {e}")
            raise DataSaveError(f"Failed to save daily data for index {symbol} to database: {e}")

    @staticmethod
    def load_concept_board_daily_data(board_data: pd.DataFrame, concept_name: str, concept_code: str):
        """
        加载概念板块日线数据到数据库
        """
        try:
            logger.info(f"Loading daily data for concept board {concept_name} to database...")
            db: Session = next(get_db())

            data_to_insert = []
            for _, row in board_data.iterrows():
                # 转换日期格式
                row_date = pd.to_datetime(row["日期"], errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row['日期']}")
                    continue

                data_to_insert.append(
                    ConceptBoardData(
                        concept_name=concept_name,
                        concept_code=concept_code,
                        date=row_date,
                        open=row["开盘"],
                        close=row["收盘"],
                        high=row["最高"],
                        low=row["最低"],
                        change_rate=row["涨跌幅"],
                        change_amount=row["涨跌额"],
                        volume=row["成交量"],
                        amount=row["成交额"],
                        amplitude=row["振幅"],
                        turnover_rate=row["换手率"]
                    )
                )

            db.bulk_save_objects(data_to_insert)
            db.commit()
            logger.info(f"Successfully saved data for concept board {concept_name}")

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save concept board data: {e}")
            raise DataSaveError(f"Failed to save concept board data: {e}")