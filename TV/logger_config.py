"""
日志配置模块
提供统一的日志配置，支持控制台输出和按日期分割的文件日志
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


def setup_logger(name: str = "tv_trader") -> logging.Logger:
    """
    配置并返回日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        配置好的Logger实例
    """
    logger = logging.getLogger(name)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 日志格式
    log_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 文件处理器 - 按日期分割，保留30天
    log_file = os.path.join(log_dir, "tv_trader.log")
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # 交易专用日志 - 单独记录所有交易操作
    trade_log_file = os.path.join(log_dir, "trades.log")
    trade_handler = TimedRotatingFileHandler(
        filename=trade_log_file,
        when="midnight",
        interval=1,
        backupCount=90,  # 交易日志保留更久
        encoding="utf-8"
    )
    trade_handler.setLevel(logging.INFO)
    trade_handler.setFormatter(log_format)

    # 创建交易专用logger
    trade_logger = logging.getLogger(f"{name}.trades")
    trade_logger.addHandler(trade_handler)
    trade_logger.setLevel(logging.INFO)

    return logger


# 创建全局logger实例
logger = setup_logger()
