from typing import Optional
from pydantic import Field

from app.config import PROJECT_ROOT
from app.config.base import BaseConfig

import os

_model_checkpoint_dir = os.environ.get("MODEL_CHECKPOINT_DIR")
_reference_voice_dir = os.environ.get("REFERENCE_VOICE_DIR")
_voice_outputs_dir = os.environ.get("VOICE_OUTPUTS_DIR")

# 检查变量是否存在
if not _model_checkpoint_dir:
    _model_checkpoint_dir = str(PROJECT_ROOT / "tts_files" / "checkpoints")

if not _reference_voice_dir:
    _reference_voice_dir = str(PROJECT_ROOT / "tts_files" / "reference_voices")

if not _voice_outputs_dir:
    _voice_outputs_dir = str(PROJECT_ROOT / "tts_files" / "outputs")

class IndexTTSConfig(BaseConfig):
    """
    IndexTTS配置类
    """
    model_checkpoint_dir: str = Field(_model_checkpoint_dir, description="模型文件所处的目录")
    reference_voice_dir: str = Field(_reference_voice_dir, description="参考音频文件所处的目录")
    voice_outputs_dir: str = Field(_voice_outputs_dir, description="默认的文件输出路径")

tts_config: IndexTTSConfig = BaseConfig.load_and_validate_config("indextts.yaml", IndexTTSConfig)