"""
测试 OSS 下载功能
"""
from download_oss import (
    download_daily_factors,
    download_year_factors,
    check_file_exists,
    list_oss_files
)


def test_check_file_exists():
    """测试检查文件是否存在"""
    print("\n" + "=" * 60)
    print("测试 1: 检查文件是否存在")
    print("=" * 60)
    
    # 测试几个可能存在的文件
    test_files = [
        "uploads/factors/2024/factors_20240101.parquet",
        "uploads/factors/2024/factors_20240102.parquet",
        "uploads/factors/2025/factors_20250101.parquet",
    ]
    
    for file_path in test_files:
        exists = check_file_exists(file_path)
        print(f"{'✓' if exists else '✗'} {file_path}")


def test_list_files():
    """测试列出文件"""
    print("\n" + "=" * 60)
    print("测试 2: 列出 OSS 文件")
    print("=" * 60)
    
    # 列出 2024 年的文件
    files = list_oss_files(prefix="uploads/factors/2024/", max_keys=20)
    print(f"\n找到 {len(files)} 个文件 (最多显示前 10 个):")
    for f in files[:10]:
        print(f"  - {f}")
    
    if len(files) > 10:
        print(f"  ... 还有 {len(files) - 10} 个文件")


def test_download_daily_factors():
    """测试下载指定日期范围的因子文件"""
    print("\n" + "=" * 60)
    print("测试 3: 下载指定日期范围的因子文件")
    print("=" * 60)
    
    # 下载 2024年1月1日 到 2024年1月3日 的因子文件（只下载3天作为测试）
    count = download_daily_factors(
        start_date="2024-01-01",
        end_date="2024-01-03",
        oss_base_prefix="uploads/factors/",
        local_base_dir="./test_data/factors/",
        file_pattern="factors_{date}.parquet"
    )
    print(f"\n✓ 成功下载 {count} 个文件到 ./test_data/factors/")


def test_download_year_factors():
    """测试下载整年的因子文件"""
    print("\n" + "=" * 60)
    print("测试 4: 下载整年的因子文件")
    print("=" * 60)
    print("注意: 这个测试会下载整年的数据，可能需要较长时间")
    print("如果不想执行，请注释掉这个测试")
    
    # 取消下面的注释来执行整年下载
    # count = download_year_factors(
    #     year=2024,
    #     oss_base_prefix="uploads/factors/",
    #     local_base_dir="./test_data/factors/"
    # )
    # print(f"\n✓ 成功下载 {count} 个文件到 ./test_data/factors/2024/")
    
    print("(已跳过，取消注释代码来执行)")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("开始测试 OSS 下载功能")
    print("=" * 60)
    
    # 运行测试
    test_check_file_exists()
    test_list_files()
    test_download_daily_factors()
    test_download_year_factors()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
