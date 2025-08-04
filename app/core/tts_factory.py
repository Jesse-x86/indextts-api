from app.config import config as app_config, AppConfig
from app.core.tts_wrapper import TTSWrapper


class TTSFactory:

    def __init__(self, config: AppConfig = app_config):
        self.config = config

    def get_tts(self) -> TTSWrapper:
        return TTSWrapper(config=self.config)
