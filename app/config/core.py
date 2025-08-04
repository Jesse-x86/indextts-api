import threading

from pydantic import BaseModel, Field

from .indextts import IndexTTSConfig
from .logger import LoggingConfig


class ConfigModel(BaseModel):
    logging: LoggingConfig = Field(..., description="Logging config")
    index_tts: IndexTTSConfig = Field(..., description="IndexTTS config")


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
        from .indextts import tts_config as index_tts_config
        return ConfigModel(
            logging=logging_config,
            index_tts=index_tts_config,
        )

    @property
    def logging(self):
        return self._config.logging

    @property
    def index_tts(self):
        return self._config.index_tts

config = AppConfig()