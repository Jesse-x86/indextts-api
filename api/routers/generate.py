from typing import Union

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.generate_speech import generate_speech

router = APIRouter(prefix="/generate", tags=["Generate Audio"])

class GenerateRequest(BaseModel):
    text: Union[str, list[str]] = Field(..., description="要生成音频的文本，单条或列表")
    speaker: Union[str, list[str]] = Field("default", description="生成音频用的说话人，单个（对所有人应用）或与文本长度一致")

@router.post("", response_model=Union[str, list[str]])
async def generate_audio_endpoint(request: GenerateRequest):
    """

    :param request:
    :return:
    """

    try:
        result = await generate_speech(text=request.text, speaker=request.speaker)

        if isinstance(request.text, str) and len(result) == 1:
            return result[0]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"音频生成失败：{str(e)}"
        )