import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.config import WORKSPACE_ROOT

OUTPUT_BASE_DIR = WORKSPACE_ROOT / "outputs"

os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

router = APIRouter()

class DownloadQueryParams(BaseModel):
    """
    下载音频文件的查询参数模型。
    """
    path: str = Field(..., alias="relative_path", description="要下载的音频文件的相对路径")


@router.get("/")
async def download_audio_file(params: DownloadQueryParams):
    relative_path = params.path

    if ".." in relative_path or relative_path.startswith('/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的文件路径。不允许使用相对路径或绝对路径。"
        )

    full_file_path = os.path.join(OUTPUT_BASE_DIR, relative_path)

    if not os.path.exists(full_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件未找到。"
        )

    if not os.path.isfile(full_file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请求的路径不是一个文件。"
        )

    return FileResponse(full_file_path, media_type="application/octet-stream",
                        filename=os.path.basename(full_file_path))
