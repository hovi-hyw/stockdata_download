# src/database/session.py
"""
数据库会话管理模块
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from src.core.config import config

# 创建数据库引擎
engine = create_engine(config.DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建数据库表
def create_tables():
    """
    创建数据库表
    """
    Base.metadata.create_all(bind=engine)


# 获取数据库会话
def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()