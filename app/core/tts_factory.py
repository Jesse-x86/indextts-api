from app.config import config as app_config, AppConfig
from app.core.tts_wrapper import TTSWrapper, TTSWrapperV1, TTSWrapperV2


class TTSFactory:

    def __init__(self, config: AppConfig = app_config):
        self.config = config

    def get_tts(self) -> TTSWrapper:
        return self.get_tts_v2()

    def get_tts_v1(self):
        return TTSWrapperV1(config=self.config)

    def get_tts_v2(self):
        return TTSWrapperV2(config=self.config)
