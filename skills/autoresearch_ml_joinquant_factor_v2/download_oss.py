"""
OSS 文件下载工具
支持按年份组织的文件夹结构，每天一个因子文件
"""
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
import oss2

# 尝试导入 python-dotenv
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# 配置日志
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def _load_oss_credentials():
    """
    从 .env 文件加载 OSS 凭证，只读取一次并缓存
    
    Returns:
        tuple: (access_key_id, access_key_secret, endpoint, bucket_name)
    """
    # 查找 .env 文件（从当前文件所在目录向上查找，直到项目根目录）
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent
    
    # 优先查找当前目录的 .env 文件
    env_file = current_dir / ".env"
    
    # 如果当前目录没有，向上查找项目根目录（查找包含 .git 或 README.md 的目录）
    if not env_file.exists():
        # 从当前目录向上查找，直到找到包含 .git 或 README.md 的目录
        search_dir = current_dir
        while search_dir.parent != search_dir:  # 直到根目录
            if (search_dir / ".git").exists() or (search_dir / "README.md").exists():
                env_file = search_dir / ".env"
                break
            search_dir = search_dir.parent
        else:
            # 如果没找到项目根目录，使用当前目录
            env_file = current_dir / ".env"
    
    # 优先从 .env 文件加载（强制从 .env 读取）
    if DOTENV_AVAILABLE and env_file.exists():
        # override=True 表示 .env 文件的值优先于环境变量
        load_dotenv(env_file, override=True)
        LOGGER.info(f"已从 .env 文件加载配置: {env_file}")
    elif env_file.exists():
        LOGGER.warning("未安装 python-dotenv，无法从 .env 文件读取配置，将使用环境变量")
    else:
        LOGGER.warning(f"未找到 .env 文件: {env_file}，将使用环境变量")
    
    # 从环境变量读取（.env 文件的值已通过 load_dotenv 加载到环境变量中）
    access_key_id = os.getenv("OSS_ACCESS_KEY_ID")
    access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET")
    endpoint = os.getenv("OSS_ENDPOINT", "https://oss-cn-hangzhou.aliyuncs.com")
    bucket_name = os.getenv("OSS_BUCKET_NAME", "test123432")
    
    return access_key_id, access_key_secret, endpoint, bucket_name


# 在模块加载时读取一次并缓存
_OSS_ACCESS_KEY_ID, _OSS_ACCESS_KEY_SECRET, _OSS_ENDPOINT, _OSS_BUCKET_NAME = _load_oss_credentials()

# 初始化 OSS 认证和 Bucket（使用缓存的凭证）
if not _OSS_ACCESS_KEY_ID or not _OSS_ACCESS_KEY_SECRET:
    LOGGER.warning("OSS 访问凭证未配置，相关函数将无法访问 OSS 资源")
    LOGGER.warning("请检查 .env 文件或环境变量中的 OSS_ACCESS_KEY_ID 和 OSS_ACCESS_KEY_SECRET")
    auth = None
    bucket = None
else:
    auth = oss2.Auth(_OSS_ACCESS_KEY_ID, _OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, _OSS_ENDPOINT, _OSS_BUCKET_NAME)
    LOGGER.info(f"OSS 已初始化: endpoint={_OSS_ENDPOINT}, bucket={_OSS_BUCKET_NAME}")


# OSS 配置
PREFIX = "uploads/"  # OSS 根目录


def list_oss_files(prefix: str = PREFIX, max_keys: int = 100) -> List[str]:
    """
    列出 OSS 指定前缀下的所有文件
    
    Args:
        prefix: OSS 文件前缀
        max_keys: 每次请求返回的最大文件数
        
    Returns:
        文件路径列表
    """
    if bucket is None:
        LOGGER.error("OSS 未初始化，无法列出文件")
        return []
    
    files = []
    marker = ""
    
    while True:
        result = bucket.list_objects(prefix=prefix, marker=marker, max_keys=max_keys)
        files.extend([obj.key for obj in result.object_list])
        
        if result.is_truncated:
            marker = result.next_marker
        else:
            break
    
    LOGGER.info(f"在 {prefix} 下找到 {len(files)} 个文件")
    return files


def download_file(oss_path: str, local_path: str) -> bool:
    """
    从 OSS 下载单个文件
    
    Args:
        oss_path: OSS 文件路径
        local_path: 本地保存路径
        
    Returns:
        是否下载成功
    """
    if bucket is None:
        LOGGER.error("OSS 未初始化，无法下载文件")
        return False
    
    try:
        # 确保本地目录存在
        local_dir = Path(local_path).parent
        local_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载文件
        bucket.get_object_to_file(oss_path, local_path)
        LOGGER.info(f"已下载: {oss_path} -> {local_path}")
        return True
    except Exception as e:
        LOGGER.error(f"下载失败 {oss_path}: {e}")
        return False


def download_daily_factors(
    start_date: str,
    end_date: str,
    oss_base_prefix: str = "uploads/factors/",
    local_base_dir: str = "./data/factors/",
    file_pattern: str = "factors_{date}.parquet"
) -> int:
    """
    下载指定日期范围内的每日因子文件
    
    OSS 文件结构示例:
        uploads/factors/2024/factors_20240101.parquet
        uploads/factors/2024/factors_20240102.parquet
        uploads/factors/2025/factors_20250101.parquet
    
    Args:
        start_date: 开始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        end_date: 结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
        oss_base_prefix: OSS 基础路径前缀
        local_base_dir: 本地保存基础目录
        file_pattern: 文件名模式，{date} 会被替换为日期（YYYYMMDD 格式）
        
    Returns:
        成功下载的文件数量
    """
    # 解析日期
    start_dt = datetime.strptime(start_date.replace('-', ''), '%Y%m%d')
    end_dt = datetime.strptime(end_date.replace('-', ''), '%Y%m%d')
    
    LOGGER.info(f"开始下载因子文件: {start_dt.date()} 到 {end_dt.date()}")
    
    success_count = 0
    current_dt = start_dt
    
    while current_dt <= end_dt:
        year = current_dt.strftime('%Y')
        date_str = current_dt.strftime('%Y%m%d')
        
        # 构建 OSS 路径和本地路径
        filename = file_pattern.format(date=date_str)
        oss_path = f"{oss_base_prefix}{year}/{filename}"
        local_path = Path(local_base_dir) / year / filename
        
        # 下载文件
        if download_file(oss_path, str(local_path)):
            success_count += 1
        
        # 移动到下一天
        current_dt += timedelta(days=1)
    
    LOGGER.info(f"下载完成: 成功 {success_count} 个文件")
    return success_count


def download_year_factors(
    year: int,
    oss_base_prefix: str = "uploads/factors/",
    local_base_dir: str = "./data/factors/"
) -> int:
    """
    下载指定年份的所有因子文件
    
    Args:
        year: 年份
        oss_base_prefix: OSS 基础路径前缀
        local_base_dir: 本地保存基础目录
        
    Returns:
        成功下载的文件数量
    """
    if bucket is None:
        LOGGER.error("OSS 未初始化，无法下载文件")
        return 0
    
    year_prefix = f"{oss_base_prefix}{year}/"
    LOGGER.info(f"开始下载 {year} 年的所有因子文件")
    
    # 列出该年份下的所有文件
    files = list_oss_files(prefix=year_prefix)
    
    success_count = 0
    for oss_path in files:
        # 提取文件名
        filename = Path(oss_path).name
        local_path = Path(local_base_dir) / str(year) / filename
        
        # 下载文件
        if download_file(oss_path, str(local_path)):
            success_count += 1
    
    LOGGER.info(f"下载完成: 成功 {success_count}/{len(files)} 个文件")
    return success_count


def check_file_exists(oss_path: str) -> bool:
    """
    检查 OSS 文件是否存在
    
    Args:
        oss_path: OSS 文件路径
        
    Returns:
        文件是否存在
    """
    if bucket is None:
        LOGGER.error("OSS 未初始化，无法检查文件")
        return False
    
    try:
        bucket.head_object(oss_path)
        return True
    except oss2.exceptions.NoSuchKey:
        return False
    except Exception as e:
        LOGGER.error(f"检查文件失败 {oss_path}: {e}")
        return False


if __name__ == "__main__":
    # 示例 1: 下载指定日期范围的因子文件
    print("=" * 60)
    print("示例 1: 下载指定日期范围的因子文件")
    print("=" * 60)
    
    # 下载 2024年1月1日 到 2024年1月7日 的因子文件
    count = download_daily_factors(
        start_date="2024-01-01",
        end_date="2024-01-07",
        oss_base_prefix="uploads/factors/",
        local_base_dir="./data/factors/",
        file_pattern="factors_{date}.parquet"
    )
    print(f"成功下载 {count} 个文件\n")
    
    # 示例 2: 下载整年的因子文件
    print("=" * 60)
    print("示例 2: 下载整年的因子文件")
    print("=" * 60)
    
    count = download_year_factors(
        year=2024,
        oss_base_prefix="uploads/factors/",
        local_base_dir="./data/factors/"
    )
    print(f"成功下载 {count} 个文件\n")
    
    # 示例 3: 检查文件是否存在
    print("=" * 60)
    print("示例 3: 检查文件是否存在")
    print("=" * 60)
    
    test_file = "uploads/factors/2024/factors_20240101.parquet"
    exists = check_file_exists(test_file)
    print(f"文件 {test_file} {'存在' if exists else '不存在'}\n")
    
    # 示例 4: 列出某个目录下的所有文件
    print("=" * 60)
    print("示例 4: 列出 2024 年的所有因子文件")
    print("=" * 60)
    
    files = list_oss_files(prefix="uploads/factors/2024/", max_keys=10)
    print(f"找到 {len(files)} 个文件:")
    for f in files[:5]:  # 只显示前5个
        print(f"  - {f}")
    if len(files) > 5:
        print(f"  ... 还有 {len(files) - 5} 个文件")
