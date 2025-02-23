# src/data_ingestion/tasks/concept_tasks.py
"""
概念板块数据任务
"""

import time
import pandas as pd
from datetime import datetime

from src.data_ingestion.fetchers.akshare_fetcher import AkShareFetcher
from src.data_ingestion.transformers.concept_transformer import ConceptTransformer
from src.data_ingestion.loaders.database_loader import DatabaseLoader
from src.core.config import config
from src.core.logger import logger
from src.utils.file_utils import check_file_validity


class ConceptTasks:
    """
    概念板块数据任务
    """

    def __init__(self):
        """
        初始化概念板块数据任务
        """
        self.fetcher = AkShareFetcher()
        self.transformer = ConceptTransformer()
        self.loader = DatabaseLoader()

    def download_and_save_concept_data(self):
        """
        下载并保存概念板块数据
        """
        # 下载概念板块
        # 1. 获取并保存概念板块列表
        today_str = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期并格式化为 YYYY-MM-DD
        concept_board_file = config.CACHE_PATH + f"/{today_str}.csv"
        if check_file_validity(concept_board_file, config.MAX_CSV_AGE_DAYS):
            logger.info("从缓存读取概念板块列表")
            concept_list = pd.read_csv(concept_board_file)
        else:
            logger.info("从API获取概念板块列表")
            concept_list = self.fetcher.fetch_concept_board_list()
            #  这里可以不用saver了，直接保存到本地
            concept_list.to_csv(concept_board_file, index=False)

        # 2. 获取并保存每个概念板块的历史数据
        for _, row in concept_list.iterrows():
            board_name = row['板块名称']
            board_code = row['板块代码']

            try:
                hist_data = self.fetcher.fetch_concept_board_daily_data(board_name, adjust='hfq')

                transformed_data = self.transformer.transform_concept_daily_data(hist_data)
                self.loader.load_concept_board_daily_data(transformed_data, board_name, board_code)

                logger.info(f"概念板块 {board_name} 日数据下载并保存完成")
                time.sleep(0.5)  # 避免请求过快
            except Exception as e:
                logger.error(f"Error processing board {board_name}: {e}")
                continue

        logger.info("概念板块数据下载任务完成")


# 示例用法
if __name__ == '__main__':
    concept_tasks = ConceptTasks()
    concept_tasks.download_and_save_concept_data()