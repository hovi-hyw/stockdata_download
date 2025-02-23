# src/database/models/concept.py
"""
概念板块数据模型
"""

from sqlalchemy import Column, String, Float, Date, Integer, PrimaryKeyConstraint
from src.database.base import Base


class ConceptBoardData(Base):
    """
    概念板块日线数据模型
    """
    __tablename__ = "concept_board"

    concept_name = Column(String, nullable=False)  # 板块名称
    concept_code = Column(String, nullable=False)  # 板块代码
    date = Column(Date, nullable=False)  # 日期
    open = Column(Float)  # 开盘
    close = Column(Float)  # 收盘
    high = Column(Float)  # 最高
    low = Column(Float)  # 最低
    change_rate = Column(Float)  # 涨跌幅
    change_amount = Column(Float)  # 涨跌额
    volume = Column(Float)  # 成交量
    amount = Column(Float)  # 成交额
    amplitude = Column(Float)  # 振幅
    turnover_rate = Column(Float)  # 换手率
    total_market_value = Column(Float)  # 总市值
    up_count = Column(Integer)  # 上涨家数
    down_count = Column(Integer)  # 下跌家数

    __table_args__ = (
        PrimaryKeyConstraint('concept_code', 'date'),
    )

    def __repr__(self):
        return f"<ConceptBoardData(concept_name={self.concept_name}, date={self.date})>"