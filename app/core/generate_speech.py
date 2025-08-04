import logging
import os.path
import uuid
from typing import Union

from app.core.tts_factory import TTSFactory

factory = TTSFactory()
logger = logging.getLogger(__name__)

async def generate_speech(text: Union[str, list[str]], speaker: Union[str, list[str]]) -> list[str]:
    if isinstance(text, str):
        text = [text]
    if isinstance(speaker, str):
        speaker = [speaker for t in text]

    if len(speaker) != len(text):
        raise

    exc_id = str(uuid.uuid4())
    tts_instance = factory.get_tts()

    successed_files = []

    for i, (t, s) in enumerate(zip(text, speaker)):
        try:
            tts_instance.infer(
                actor=s,
                text=t,
                subfolder=exc_id,
                filename=f"{i}.wav"  # 使用 f-string 来格式化文件名
            )
            successed_files.append(
                os.path.join(exc_id, f"{i}.wav")
            )
        except Exception as e:
            logger.error(f"Error generating speech for text {i}: {e}")
            pass

    return successed_files