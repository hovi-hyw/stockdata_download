# src/data_ingestion/loaders/database_loader.py
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.session import get_db
from src.database.models.stock import StockDailyData
from src.core.logger import logger
from src.core.exceptions import DataSaveError
from src.core.config import config


class DatabaseLoader:
    """数据库加载器"""

    @staticmethod
    def load_stock_daily_data(stock_data: pd.DataFrame, symbol: str):
        """加载股票日线数据到数据库，包含批量插入和冲突处理"""
        logger.info(f"Loading daily data for stock {symbol} to database...")
        db: Session = next(get_db())
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

        try:
            # 使用 SQLAlchemy 的 bulk_insert_mappings 方法
            db.bulk_insert_mappings(StockDailyData, [data.__dict__ for data in data_to_insert])
            db.commit()
            logger.info(f"Inserted {len(data_to_insert)} new records for stock {symbol}.")

        except IntegrityError as e:
            db.rollback()
            # 唯一约束冲突，记录冲突信息，然后跳过冲突的记录
            logger.warning(f"IntegrityError encountered while saving data for stock {symbol}: {e}")

            # 详细记录重复的键值
            logger.warning(f"Failed to save daily data for stock {symbol} to database: {e}")

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save daily data for stock {symbol} to database: {e}")
            raise DataSaveError(f"Failed to save daily data for stock {symbol} to database: {e}")