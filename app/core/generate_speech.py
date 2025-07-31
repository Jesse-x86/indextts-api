from typing import Union


async def generate_speech(text: Union[str, list[str]], speaker: Union[str, list[str]]):
    if isinstance(text, str):
        text = [text]
    if isinstance(speaker, str):
        speaker = [speaker for t in text]

    if len(speaker) != len(text):
        raise

    for t, s in zip(text, speaker):
        pass

async def _generate_speech(text: str, speaker: str, output_file: str):
    pass