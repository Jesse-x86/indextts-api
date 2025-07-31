# FastAPI 应用的主文件，负责注册路由

from fastapi import FastAPI
from .routers import generate, download
from app.config import PROGRAM_NAME, PROGRAM_DESC, PROGRAM_VERSION

# 创建 FastAPI 应用实例
app = FastAPI(
    title=PROGRAM_NAME,
    description=PROGRAM_DESC,
    version=PROGRAM_VERSION,
)

# 注册路由
app.include_router(generate.router, prefix="/generate", tags=["Generate Audio"])
app.include_router(download.router, prefix="/download", tags=["Download Audio"])