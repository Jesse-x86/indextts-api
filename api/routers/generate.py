from typing import Union

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.generate_speech import generate_speech  # 假设这是你的音频生成核心函数

# 为每个版本创建独立的 APIRouter
router_v1 = APIRouter(prefix="/v1", tags=["Generate Audio (v1)"])
router_v2 = APIRouter(prefix="/v2", tags=["Generate Audio (v2)"])

# 创建一个用于向后兼容的路由器
router_legacy = APIRouter(prefix="", tags=["Generate Audio (Legacy)"])


class GenerateRequestV1(BaseModel):
    text: Union[str, list[str]] = Field(..., description="要生成音频的文本，单条或列表")
    speaker: Union[str, list[str]] = Field("default", description="生成音频用的说话人，单个（对所有人应用）或与文本长度一致")


class GenerateRequestV2(BaseModel):
    text: Union[str, list[str]] = Field(..., description="要生成音频的文本，单条或列表")
    speaker: Union[str, list[str]] = Field("default", description="生成音频用的说话人，单个（对所有人应用）或与文本长度一致")


@router_v1.post("/generate", response_model=Union[str, list[str]])
async def generate_audio_v1_endpoint(request: GenerateRequestV1):
    """
    音频生成接口 (v1版本)

    根据提供的文本和说话人生成音频。
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


@router_v2.post("/generate", response_model=Union[str, list[str]])
async def generate_audio_v2_endpoint(request: GenerateRequestV2):
    """
    音频生成接口 (v2版本)

    根据提供的文本和说话人生成音频。
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


# 向后兼容接口，它直接调用 v2 版本的处理函数
@router_legacy.post("/generate", response_model=Union[str, list[str]])
async def generate_audio_legacy_endpoint(request: GenerateRequestV2):
    """
    音频生成接口 (向后兼容)

    此接口直接调用 v2 版本的逻辑，以保持与旧客户端的兼容性。
    """
    return await generate_audio_v2_endpoint(request)