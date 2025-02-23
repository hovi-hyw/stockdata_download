# src/data_ingestion/tasks/index_tasks.py
"""
指数数据任务
"""

import pandas as pd
from datetime import datetime
from src.data_ingestion.fetchers.akshare_fetcher import AkShareFetcher
from src.data_ingestion.transformers.index_transformer import IndexTransformer
from src.data_ingestion.loaders.database_loader import DatabaseLoader
from src.core.config import config
from src.core.logger import logger
from src.utils.file_utils import check_file_validity


class IndexTasks:
    """
    指数数据任务
    """

    def __init__(self):
        """
        初始化指数数据任务
        """
        self.fetcher = AkShareFetcher()
        self.transformer = IndexTransformer()
        self.loader = DatabaseLoader()

    def format_index_code(self, symbol):
        """确保指数代码为6位数字格式"""
        return str(symbol).zfill(6)

    def download_and_save_index_data(self):
        """
        下载并保存指数数据
        """
        # 获取指数列表
        if check_file_validity(config.CACHE_PATH + "/index_list.csv", config.MAX_CSV_AGE_DAYS):
            logger.info("从缓存读取指数列表")
            index_list = pd.read_csv(config.CACHE_PATH + "/index_list.csv")
        else:
            logger.info("从东方财富获取指数列表")
            index_list = self.fetcher.fetch_index_list()
            #  这里可以不用saver了，直接保存到本地
            index_list.to_csv(config.CACHE_PATH + "/index_list.csv", index=False)

        # 下载指数日数据并保存到数据库
        for _, row in index_list.iterrows():
            symbol = row["代码"]
            name = row["名称"]
            formatted_symbol = self.format_index_code(symbol)
            try:
                index_data = self.fetcher.fetch_index_daily_data(
                    formatted_symbol,
                    config.AKSHARE_DATA_START_DATE,
                    datetime.today().strftime("%Y%m%d")
                )
                if index_data is None:
                    logger.warning(f"未能获取到指数 {formatted_symbol}({name}) 的数据")
                    continue

                transformed_data = self.transformer.transform_index_daily_data(index_data)
                self.loader.load_index_daily_data(transformed_data, formatted_symbol, name)

                logger.info(f"指数 {formatted_symbol}({name}) 日数据下载并保存完成")
            except Exception as e:
                logger.error(f"处理指数 {formatted_symbol}({name}) 时出错: {e}")
                continue

        logger.info("指数数据下载任务完成")


# 示例用法
if __name__ == '__main__':
    index_tasks = IndexTasks()
    index_tasks.download_and_save_index_data()