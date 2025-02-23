# scripts/run_tasks.py
"""
运行数据摄取任务的脚本
"""

import argparse
from src.data_ingestion.tasks.stock_tasks import StockTasks
from src.data_ingestion.tasks.index_tasks import IndexTasks
from src.data_ingestion.tasks.concept_tasks import ConceptTasks
from src.core.logger import logger
from src.utils.db_utils import initialize_database_if_needed


def main():
    """
    主函数
    """
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

    if args.task == "all":
        run_all_tasks()
    elif args.task == "stock":
        run_stock_task()
    elif args.task == "index":
        run_index_task()
    elif args.task == "concept":
        run_concept_task()
    else:
        logger.error("无效的任务类型")


def run_all_tasks():
    """
    运行所有数据摄取任务
    """
    run_stock_task()
    run_index_task()
    run_concept_task()


def run_stock_task():
    """
    运行股票数据摄取任务
    """
    logger.info("开始运行股票数据摄取任务...")
    stock_tasks = StockTasks()
    stock_tasks.download_and_save_stock_data()
    logger.info("股票数据摄取任务完成")


def run_index_task():
    """
    运行指数数据摄取任务
    """
    logger.info("开始运行指数数据摄取任务...")
    index_tasks = IndexTasks()
    index_tasks.download_and_save_index_data()
    logger.info("指数数据摄取任务完成")


def run_concept_task():
    """
    运行概念板块数据摄取任务
    """
    logger.info("开始运行概念板块数据摄取任务...")
    concept_tasks = ConceptTasks()
    concept_tasks.download_and_save_concept_data()
    logger.info("概念板块数据摄取任务完成")


if __name__ == "__main__":
    main()