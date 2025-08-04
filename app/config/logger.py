from typing import Optional
from pydantic import Field

from .base import BaseConfig

class LoggingConfig(BaseConfig):
    """
    日志配置类
    """
    console_level: str = Field("INFO", description="日志级别")
    file_level: Optional[str] = Field(None, description="日志文件级别")
    file: Optional[str] = Field(None, description="日志文件路径")
    format: str = Field("%(name)s - %(asctime)s - %(levelname)s - [%(module)s - Line %(lineno)d] - %(message)s",
                        description="日志格式")
    max_size: int = Field(10, description="日志文件最大大小（MB）")
    backup_count: int = Field(3, description="日志文件备份数量")

logging_config: LoggingConfig = BaseConfig.load_and_validate_config("logging.yaml", LoggingConfig)