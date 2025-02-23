# src/data_ingestion/tasks/stock_tasks.py
"""
股票数据任务
"""

import pandas as pd
from datetime import datetime
from src.data_ingestion.fetchers.akshare_fetcher import AkShareFetcher
from src.data_ingestion.transformers.stock_transformer import StockTransformer
from src.data_ingestion.loaders.database_loader import DatabaseLoader
from src.core.config import config
from src.core.logger import logger
from src.utils.file_utils import check_file_validity


class StockTasks:
    """
    股票数据任务
    """

    def __init__(self):
        """
        初始化股票数据任务
        """
        self.fetcher = AkShareFetcher()
        self.transformer = StockTransformer()
        self.loader = DatabaseLoader()

    def download_and_save_stock_data(self):
        """
        下载并保存股票数据
        """
        # 获取股票列表
        if check_file_validity(config.CACHE_PATH + "/stock_list.csv", config.MAX_CSV_AGE_DAYS):
            logger.info("从缓存读取股票列表")
            stock_list = pd.read_csv(config.CACHE_PATH + "/stock_list.csv")
        else:
            logger.info("从API获取股票列表")
            stock_list = self.fetcher.fetch_stock_list()
            #  这里可以不用saver了，直接保存到本地
            stock_list.to_csv(config.CACHE_PATH + "/stock_list.csv", index=False)

        # 下载股票日数据并保存到数据库
        for symbol in stock_list["代码"]:
            try:
                stock_data = self.fetcher.fetch_stock_daily_data(symbol, "20040101",
                                                                 datetime.today().strftime("%Y%m%d"), 'hfq')
                transformed_data = self.transformer.transform_stock_daily_data(stock_data)
                self.loader.load_stock_daily_data(transformed_data, symbol)
                logger.info(f"股票 {symbol} 日数据下载并保存完成")
            except Exception as e:
                logger.error(f"下载股票{symbol}数据失败: {e}")
                continue

        logger.info("股票数据下载任务完成")


# 示例用法
if __name__ == '__main__':
    stock_tasks = StockTasks()
    stock_tasks.download_and_save_stock_data()