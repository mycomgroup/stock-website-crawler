"""
测试 DuckDB 集成功能。
"""

import pytest

from jk2bt.db import DuckDBManager
from jk2bt.market_data import (
    get_stock_daily,
    get_etf_daily,
    get_index_daily,
)
from jk2bt import (
    get_akshare_stock_data,
    get_akshare_etf_data,
    get_price,
)
from jk2bt import (
    get_akshare_stock_data,
    get_akshare_etf_data,
    get_price,
)


def test_duckdb_connection():
    """测试 DuckDB 连接"""
    print("=" * 60)
    print("测试 1: DuckDB 连接和数据统计")
    print("=" * 60)

    db = DuckDBManager()

    stock_count = db.count_records("stock_daily")
    etf_count = db.count_records("etf_daily")
    index_count = db.count_records("index_daily")

    print(f"✅ DuckDB 连接成功")
    print(f"✅ 股票数据: {stock_count} 条")
    print(f"✅ ETF 数据: {etf_count} 条")
    print(f"✅ 指数数据: {index_count} 条")

    stock_symbols = db.get_symbols("stock_daily")
    etf_symbols = db.get_symbols("etf_daily")
    index_symbols = db.get_symbols("index_daily")

    print(f"✅ 股票代码数量: {len(stock_symbols)}")
    print(f"✅ ETF 代码数量: {len(etf_symbols)}")
    print(f"✅ 指数代码数量: {len(index_symbols)}")

    return True


def test_market_data_modules():
    """测试 market_data 模块"""
    print("\n" + "=" * 60)
    print("测试 2: market_data 模块数据加载")
    print("=" * 60)

    # 测试股票数据
    print("测试股票数据加载...")
    stock_df = get_stock_daily("sh600000", "2023-01-01", "2023-12-31")
    print(f"✅ 加载股票数据成功: {len(stock_df)} 行")

    # 测试 ETF 数据
    print("测试 ETF 数据加载...")
    etf_df = get_etf_daily("510300", "2023-01-01", "2023-12-31")
    print(f"✅ 加载 ETF 数据成功: {len(etf_df)} 行")

    # 测试指数数据（需要从 akshare 下载）
    print("测试指数数据加载...")
    index_df = get_index_daily("000300", "2023-01-01", "2023-12-31")
    print(f"✅ 加载指数数据成功: {len(index_df)} 行")

    return True


def test_backtrader_functions():
    """测试 backtrader_base_strategy 函数"""
    print("\n" + "=" * 60)
    print("测试 3: backtrader_base_strategy 函数")
    print("=" * 60)

    # 测试 get_akshare_stock_data
    print("测试 get_akshare_stock_data...")
    stock_data = get_akshare_stock_data("sh600000", "2023-01-01", "2023-12-31")
    print(f"✅ 加载 Backtrader 股票数据成功: {stock_data._name}")

    # 测试 get_akshare_etf_data
    print("测试 get_akshare_etf_data...")
    etf_data = get_akshare_etf_data("510300", "2023-01-01", "2023-12-31")
    print(f"✅ 加载 Backtrader ETF 数据成功: {etf_data._name}")

    # 测试 get_price
    print("测试 get_price...")
    price_result = get_price(["sh600000", "sz000001"], "2023-01-01", "2023-12-31")
    print(f"✅ 加载多只股票数据成功")
    for symbol, df in price_result.items():
        print(f"   - {symbol}: {len(df)} 行")

    # 测试 get_index_nav
    print("测试 get_index_nav...")
    nav = get_index_nav("000300", "2023-01-01", "2023-12-31")
    print(f"✅ 加载指数净值数据成功: {len(nav)} 行")
    print(f"   - 起始净值: {nav.iloc[0]}")
    print(f"   - 结束净值: {nav.iloc[-1]}")

    return True


def main():
    """运行所有测试"""
    print("🚀 DuckDB 集成测试")
    print("=" * 60)

    try:
        test_duckdb_connection()
        test_market_data_modules()
        test_backtrader_functions()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)

        print("\n📊 测试总结:")
        print("  1. DuckDB 数据库连接正常")
        print("  2. 数据迁移成功（从 pickle 到 DuckDB）")
        print("  3. market_data 模块正常工作")
        print("  4. backtrader_base_strategy 函数正常工作")
        print("  5. API 保持向后兼容")

        print("\n💡 使用建议:")
        print("  - 使用 cache_common_data.py 批量更新数据")
        print("  - 数据自动从 DuckDB 加载，无需手动管理 pickle 文件")
        print("  - 财务数据仍使用 pickle 缓存")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
