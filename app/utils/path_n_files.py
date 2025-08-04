import os
import re
import time

from app.config import PROJECT_ROOT


def format_filename(filename: str, target_time: time.struct_time = time.localtime()) -> str:
    filename = (filename
                .replace("%datetime%", time.strftime("%Y年%m月%d日%H时%M分%S秒", target_time))
                .replace("%date%", time.strftime("%Y年%m月%d日", target_time))
                .replace("%time%", time.strftime("%H时%M分%S秒", target_time))
                )
    return filename


def path_to_abs_path(file_path: str, base_path: str = PROJECT_ROOT) -> str:
    if os.path.isabs(file_path):
        return file_path
    return os.path.abspath(os.path.join(base_path, file_path))


def ensure_parents_exist(file_path: str) -> None:
    dir_path = os.path.dirname(file_path)
    if dir_path:
        ensure_dir_exist(dir_path)

def ensure_dir_exist(file_dir: str) -> None:
    file_dir = path_to_abs_path(file_dir)
    if not os.path.exists(file_dir):
        try:
            os.makedirs(file_dir, exist_ok=True)
        except Exception as e:
            pass


def normalize_filename(name: str, postfix: str = None) -> str:
    """
    标准化一个字符串，使其适合作为文件名或路径的一部分，
    保留合法的非 ASCII 字符，只替换非法或不安全的字符。

    :param name: 待标准化的字符串。
    :param postfix: 后缀名，如果提供，会在标准化后添加到文件名的末尾。不含点号。

    :returns: 标准化后的文件名（不含扩展名）。

    """

    # 1. 移除开头和结尾的空格（文件系统通常会trim）
    cleaned_name = name.strip()

    # 2. 移除文件扩展名
    cleaned_name = os.path.splitext(cleaned_name)[0]

    # 3. 替换文件系统中非法或不安全的字符为下划线
    #   [\x00-\x1f]：匹配控制字符
    #   [<>:"/\\|?*]：匹配 Windows 和 POSIX 系统中的常见非法字符
    #   [ \t\n\r\f\v]：匹配空白字符（如空格、制表符等）
    #   \.$：匹配字符串末尾的点号（Windows 上的特殊处理）
    # 注意：这里移除了连字符 '-' 的特殊处理，因为它通常是合法的
    cleaned_name = re.sub(r'[\x00-\x1f<>:"/\\|?*\t\n\r\f\v]', '_', cleaned_name)

    # 4. 替换字符串末尾的点号（Windows 文件名不能以点号结尾）
    cleaned_name = re.sub(r'\.$', '_', cleaned_name)

    # 5. 替换连续的下划线为单个下划线
    cleaned_name = re.sub(r'_{2,}', '_', cleaned_name)

    # 6. 如果标准化后为空，给一个默认值
    if not cleaned_name:
        # _logger.warning(f"Normalized name for original '{name}' resulted in an empty string. Returning 'unnamed_file'.")
        return "unnamed_file"

    # 7. 添加后缀名
    if postfix:
        cleaned_name = f"{cleaned_name}.{postfix}"

    # _logger.debug(f"Normalized '{name}' to '{cleaned_name}'.")
    return cleaned_name