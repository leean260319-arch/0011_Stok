"""TC01-01.T003 - 로깅 모듈 테스트"""
import logging
import os
import tempfile

import pytest


class TestLogger:
    """src/utils/logger.py 단위 테스트"""

    def test_get_logger_returns_logger(self):
        from src.utils.logger import get_logger

        logger = get_logger("test")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "stokai.test"

    def test_get_logger_has_console_handler(self):
        from src.utils.logger import get_logger

        logger = get_logger("console_test")
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" in handler_types

    def test_get_logger_has_file_handler(self):
        from src.utils.logger import get_logger

        logger = get_logger("file_test")
        handler_types = [type(h).__name__ for h in logger.handlers]
        has_file = any("FileHandler" in t or "RotatingFileHandler" in t
                       or "TimedRotatingFileHandler" in t for t in handler_types)
        assert has_file

    def test_logger_default_level_is_debug(self):
        from src.utils.logger import get_logger

        logger = get_logger("level_test")
        assert logger.level == logging.DEBUG

    def test_logger_utf8_encoding(self):
        from src.utils.logger import get_logger

        logger = get_logger("utf8_test")
        for handler in logger.handlers:
            if hasattr(handler, "encoding"):
                assert handler.encoding == "utf-8"

    def test_logger_format_includes_timestamp(self):
        from src.utils.logger import LOG_FORMAT

        assert "asctime" in LOG_FORMAT

    def test_setup_logging_creates_log_dir(self):
        from src.utils.logger import setup_logging

        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = os.path.join(tmpdir, "logs")
            setup_logging(log_dir=log_dir)
            assert os.path.isdir(log_dir)
