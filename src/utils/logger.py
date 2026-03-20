"""StokAI 로깅 모듈 - 파일 + 콘솔 동시 출력, 일별 로테이션, UTF-8"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.utils.constants import LOG_DIR

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_initialized_loggers = set()


def setup_logging(log_dir=None, level=logging.DEBUG):
    if log_dir is None:
        log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_logger(name, log_dir=None, level=logging.DEBUG):
    if log_dir is None:
        log_dir = LOG_DIR
    logger_name = f"stokai.{name}"

    if logger_name in _initialized_loggers:
        return logging.getLogger(logger_name)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "stokai.log")
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=90,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _initialized_loggers.add(logger_name)
    return logger
