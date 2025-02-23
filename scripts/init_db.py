# scripts/init_db.py
"""
初始化数据库脚本
"""
import time
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from src.database.session import engine, Base
from src.core.logger import logger
from src.core.config import config


def init_database():
    """初始化数据库，创建所有表，包含重试机制"""
    for attempt in range(config.DB_INIT_MAX_RETRIES):
        try:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            all_tables = Base.metadata.tables.keys()
            missing_tables = [table for table in all_tables if table not in existing_tables]

            if not missing_tables:
                logger.info("所有表都已存在，跳过创建步骤。")
                return  # 提前退出，避免不必要的重试
            else:
                logger.info(f"以下表不存在，将创建这些表: {missing_tables}")
                Base.metadata.create_all(bind=engine)
                logger.info("数据库表创建成功！")
                return  # 成功后退出循环

        except SQLAlchemyError as e:  # 捕获SQLAlchemy特定的异常
            logger.error(f"创建数据库表时发生错误 (尝试 {attempt + 1}/{config.DB_INIT_MAX_RETRIES}): {str(e)}")
            if attempt < config.DB_INIT_MAX_RETRIES - 1:
                time.sleep(config.DB_INIT_RETRY_DELAY)  # 等待一段时间后重试
            else:
                logger.error("达到最大重试次数，数据库初始化失败。")
                raise  # 最终还是抛出异常，让调用者知道失败了
        except Exception as e:
            logger.error(f"创建数据库表时发生未知错误: {str(e)}")
            raise


if __name__ == '__main__':
    init_database()