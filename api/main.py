# FastAPI 应用的主文件，负责注册路由

from fastapi import FastAPI

from app.utils.logger import setup_app_logger
from .routers import generate, download
from app.config import PROGRAM_NAME, PROGRAM_DESC, PROGRAM_VERSION, config

# 创建 FastAPI 应用实例
app = FastAPI(
    title=PROGRAM_NAME,
    description=PROGRAM_DESC,
    version=PROGRAM_VERSION,
)

# 注册路由
app.include_router(generate.router)
app.include_router(download.router)

setup_app_logger(config=config)