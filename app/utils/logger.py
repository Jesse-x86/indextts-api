import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import AppConfig
from app.utils.path_n_files import format_filename, path_to_abs_path, ensure_parents_exist


def setup_logger(config: AppConfig, logger: logging.Logger):
    _config = config.logging
    _handlers_added = False

    # 设置 logger 的级别
    logger.setLevel(
        min(logging._nameToLevel[_config.console_level.upper()], logging._nameToLevel[_config.file_level.upper()])
        if _config.file_level
        else logging._nameToLevel[_config.console_level.upper()]
    )

    formatter = logging.Formatter(_config.format)

    # 如果应该有控制台日志，创建并添加处理器
    if _config.console_level.upper() != "NONE":
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(_config.console_level.upper())
        logger.addHandler(console_handler)
        _handlers_added = True

    # 如果应该有文件日志
    if _config.file and _config.file_level.upper() != "NONE":
        try:
            filename = format_filename(_config.file)
            filename = path_to_abs_path(filename)
            ensure_parents_exist(filename)

            file_handler = RotatingFileHandler(
                filename,
                maxBytes=_config.max_size * 1024 * 1024,
                backupCount=_config.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_level = _config.file_level or _config.console_level
            file_handler.setLevel(file_level.upper())

            logger.addHandler(file_handler)
            _handlers_added = True
        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"[LOGGER_WARNING] Failed to create log file '{filename}': {e}", file=sys.stderr)
            pass

    # 如果没有添加任何处理器，添加一个 NullHandler
    if not _handlers_added:
        logger.addHandler(logging.NullHandler())
    return logger

def setup_app_logger(config: AppConfig):
    return setup_logger(config=config, logger=logging.getLogger("app"))