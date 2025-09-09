import os.path
from abc import abstractmethod, ABC

from indextts.infer import IndexTTS
from indextts.infer_v2 import IndexTTS2

from app.config import AppConfig


class TTSWrapper(ABC):

    @abstractmethod
    def infer(self, actor: str, text: str, subfolder: str, filename: str):
        pass

class TTSWrapperV1(TTSWrapper):

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

class TTSWrapperV2(TTSWrapper):

    def __init__(self, config: AppConfig):
        self._config = config
        self._instance = IndexTTS2(model_dir=self._config.index_tts.model_v2_checkpoint_dir,
                                   cfg_path=os.path.join(self._config.index_tts.model_v2_checkpoint_dir, "config.yaml"),
                                   is_fp16=False,
                                   use_cuda_kernel=False)

    def infer(self, actor: str, text: str, subfolder: str, filename: str):
        voice = os.path.join(self._config.index_tts.reference_voice_dir,
                             actor + ".wav")
        output_path = os.path.join(self._config.index_tts.voice_outputs_dir,
                                   subfolder,
                                   filename)
        return self._instance.infer(spk_audio_prompt=voice, text=text, output_path=output_path, verbose=True)