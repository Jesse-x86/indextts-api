import logging
import os.path
import uuid
from typing import Union

import torch

from app.core.tts_factory import TTSFactory
import gc  # 导入 gc 模块用于垃圾回收

factory = TTSFactory()
logger = logging.getLogger(__name__)


async def generate_speech(
        text: Union[str, list[str]],
        speaker: Union[str, list[str]],
        version: str = "v1"  # 新增的参数，默认为 'v1'
) -> list[str]:
    """
    根据文本和说话人生成语音文件。

    Args:
        text (Union[str, list[str]]): 要生成音频的文本，可以是单条或列表。
        speaker (Union[str, list[str]]): 生成音频用的说话人，可以是单个或与文本长度一致的列表。
        version (str): 指定使用的 TTS 版本，'v1' 或 'v2'。默认为 'v1'。

    Returns:
        list[str]: 成功生成的音频文件路径列表。
    """
    if isinstance(text, str):
        text = [text]
    if isinstance(speaker, str):
        speaker = [speaker] * len(text)

    if len(speaker) != len(text):
        raise ValueError("文本和说话人的数量不匹配。")

    exc_id = str(uuid.uuid4())
    tts_instance = None  # 初始化为 None

    try:
        if version == "v2":
            tts_instance = factory.get_tts_v2()
        else:
            # 默认或 'v1' 的情况都使用 v1
            tts_instance = factory.get_tts_v1()

        successed_files = []
        for i, (t, s) in enumerate(zip(text, speaker)):
            try:
                tts_instance.infer(
                    actor=s,
                    text=t,
                    subfolder=exc_id,
                    filename=f"{i}.wav"
                )
                successed_files.append(
                    os.path.join(exc_id, f"{i}.wav")
                )
            except Exception as e:
                logger.error(f"Error generating speech for text {i}: {e}")
                pass

        return successed_files

    finally:
        # 无论成功或失败，都在函数结束时强制进行内存回收
        del tts_instance
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()