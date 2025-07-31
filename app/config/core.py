import threading

from pydantic import BaseModel, Field

from app.config.base import BaseConfig
from app.config.logger import LoggingConfig


class ConfigModel(BaseModel):
    logging: LoggingConfig = Field(..., description="Logging config")


class AppConfig:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config: ConfigModel = self._initialize()
                    self._initialized = True

    @staticmethod
    def _initialize():
        from .logger import logging_config
        return ConfigModel(
            logging=logging_config
        )

    @property
    def logging(self):
        return self._config.logging

config = AppConfig()