"""
项目路径工具模块
提供基于项目根目录的绝对路径解析，避免相对路径导致的数据写入位置错误。
"""

import os
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录（jk2bt-main 目录）"""
    return Path(__file__).parent.parent.parent


def resolve_cache_path(relative_path: str) -> str:
    """
    将相对缓存路径解析为基于项目根目录的绝对路径。

    Args:
        relative_path: 相对于项目根目录的路径，如 "data_cache/market.db"

    Returns:
        绝对路径字符串
    """
    return str(get_project_root() / relative_path)


def resolve_cache_dir(relative_path: str) -> Path:
    """
    将相对缓存目录路径解析为基于项目根目录的 Path 对象。

    Args:
        relative_path: 相对于项目根目录的路径，如 "data_cache/cache"

    Returns:
        Path 对象
    """
    return get_project_root() / relative_path
