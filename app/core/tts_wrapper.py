import os.path

from indextts.infer import IndexTTS

from app.config import AppConfig


class TTSWrapper:

    _instance: IndexTTS

    def __init__(self, config: AppConfig):
        self._config = config
        self._instance = IndexTTS(model_dir=self._config.index_tts.model_checkpoint_dir,
                                  cfg_path=os.path.join(self._config.index_tts.model_checkpoint_dir, "config.yaml"))

    def infer(self, actor: str, text: str, subfolder: str, filename: str):
        voice = os.path.join(self._config.index_tts.reference_voice_dir,
                             actor + ".wav")
        output_path = os.path.join(self._config.index_tts.voice_outputs_dir,
                                   subfolder,
                                   filename)
        return self._instance.infer(voice, text, output_path)