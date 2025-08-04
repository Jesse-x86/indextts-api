from pathlib import Path
from typing import TypeVar, ClassVar

import yaml
from pydantic import BaseModel, ValidationError


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).resolve().parent.parent.parent


PROJECT_ROOT = get_project_root()
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
PROGRAM_NAME = "index-tts-api"
PROGRAM_DESC = "一个用于生成和下载音频的简单 API。"
PROGRAM_VERSION = "0.0.1"


class BaseConfig(BaseModel):
    """
    基础配置类，所有配置类都应该继承自这个类。
    """

    configType: ClassVar = TypeVar("configType", bound='BaseConfig')
    @staticmethod
    def load_and_validate_config(
            filename: str,
            config_model: type[configType]
    ) -> configType:
        """
        统一的配置加载和验证方法。
        :param filename: 配置文件的名称
        :param config_model: 用于验证配置的Pydantic模型类
        :return: BaseConfig：验证后的配置对象
        """
        if not filename.endswith(".yaml"):
            filename += ".yaml"
        config_path = PROJECT_ROOT / "config" / filename
        example_config_path = PROJECT_ROOT / "config" / f"{filename.split('.')[0]}.example.yaml"

        target_path: Path = Path()

        if config_path.exists():
            target_path = config_path
        elif example_config_path.exists():
            target_path = example_config_path
        else:
            try:
                return config_model()
            except ValidationError as exc:
                raise FileNotFoundError(
                    f"Config file '{filename}' or example config file '{example_config_path.name}' not found "
                    f"in '{PROJECT_ROOT / 'config'}'. Attempt to create blank config FAILED. FATAL ERROR."
                )

        with open(target_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        try:
            # 使用 Pydantic 模型验证并解析配置
            return config_model(**raw_config)
        except ValidationError as e:
            print(f"Error validating config file '{target_path.name}': {e}")
            raise  # 重新抛出异常，以便上层捕获和处理
