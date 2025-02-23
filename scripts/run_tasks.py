# scripts/run_tasks.py
import argparse
import logging
import time
from src.data_ingestion.tasks.stock_tasks import StockTasks
from src.data_ingestion.tasks.index_tasks import IndexTasks
from src.data_ingestion.tasks.concept_tasks import ConceptTasks
from src.core.logger import logger
from src.utils.db_utils import initialize_database_if_needed
from src.core.config import config


def run_task_with_retry(task_func, task_name):
    """运行任务，如果失败则重试。"""
    for attempt in range(config.MAX_RETRIES):
        try:
            logger.info(f"开始运行 {task_name} (尝试 {attempt + 1}/{config.MAX_RETRIES})")
            task_func()
            logger.info(f"{task_name} 任务完成")
            return  # 任务成功，退出循环
        except Exception as e:
            logger.error(f"{task_name} 任务失败 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {e}")
            if attempt < config.MAX_RETRIES - 1:
                logger.info(f"等待 {config.RETRY_DELAY} 秒后重试...")
                time.sleep(config.RETRY_DELAY)
            else:
                logger.error(f"{task_name} 任务达到最大重试次数，放弃。")


def main():
    initialize_database_if_needed()
    parser = argparse.ArgumentParser(description="运行数据摄取任务")
    parser.add_argument(
        "--task",
        type=str,
        choices=["all", "stock", "index", "concept"],
        default="all",
        help="要运行的任务类型 (all, stock, index, concept)",
    )
    args = parser.parse_args()

    # 使用字典映射任务类型到函数，避免重复的 if/elif 结构
    task_map = {
        "all": lambda: [run_task_with_retry(StockTasks().download_and_save_stock_data, "股票数据摄取"),
                        run_task_with_retry(IndexTasks().download_and_save_index_data, "指数数据摄取"),
                        run_task_with_retry(ConceptTasks().download_and_save_concept_data, "概念板块数据摄取")],
        "stock": lambda: run_task_with_retry(StockTasks().download_and_save_stock_data, "股票数据摄取"),
        "index": lambda: run_task_with_retry(IndexTasks().download_and_save_index_data, "指数数据摄取"),
        "concept": lambda: run_task_with_retry(ConceptTasks().download_and_save_concept_data, "概念板块数据摄取")
    }

    task_action = task_map.get(args.task)
    if task_action:
        task_action()
    else:
        logger.error("无效的任务类型")


if __name__ == "__main__":
    main()