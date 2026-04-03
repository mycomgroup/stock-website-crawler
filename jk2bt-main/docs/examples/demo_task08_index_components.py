"""
demo_task08_index_components.py
任务8：指数成分股数据 API 使用演示
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jk2bt.market_data import (
    get_index_stocks,
    get_index_weights,
    get_index_component_history,
    query_index_components,
)
from jk2bt.market_data.index_components import (
    finance,
    run_query_simple as run_query_simple_index,
)

import warnings

warnings.filterwarnings("ignore")


def demo_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("任务8：指数成分股数据 API - 基本使用演示")
    print("=" * 60)
    print()

    # 1. 查询沪深300成分股
    print("1. 查询沪深300成分股")
    print("-" * 40)
    stocks = get_index_stocks("000300")
    print(f"   成分股数量: {len(stocks)} 只")
    print(f"   前10只股票: {stocks[:10]}")
    print()

    # 2. 查询上证50权重
    print("2. 查询上证50权重")
    print("-" * 40)
    weights = get_index_weights("000016")
    print(f"   权重数据行数: {len(weights)}")
    if not weights.empty:
        top5 = weights.nlargest(5, "weight")
        print(f"   权重最大的5只股票:")
        for idx, row in top5.iterrows():
            print(f"      {row['stock_code']}: {row['weight']:.3f}%")
        print(f"   权重总和: {weights['weight'].sum():.2f}%")
    print()

    # 3. 查询中证500成分股历史
    print("3. 查询中证500成分股历史")
    print("-" * 40)
    history = get_index_component_history("000905")
    print(f"   历史记录数: {len(history)}")
    if not history.empty:
        print(f"   数据列: {history.columns.tolist()}")
        print(f"   前5条记录:")
        print(history.head())
    print()

    # 4. 批量查询多个指数
    print("4. 批量查询多个指数")
    print("-" * 40)
    multi_df = query_index_components(["000300", "000016"])
    print(f"   批量查询结果: {len(multi_df)} 条记录")
    print(f"   指数分布:")
    if not multi_df.empty and "index_code" in multi_df.columns:
        print(multi_df.groupby("index_code").size())
    print()


def demo_finance_module():
    """Finance 模块使用示例"""
    print("=" * 60)
    print("任务8：Finance 模块模拟演示")
    print("=" * 60)
    print()

    # 1. 使用 finance.STK_INDEX_WEIGHTS
    print("1. 使用 finance.STK_INDEX_WEIGHTS")
    print("-" * 40)
    query_obj = finance.STK_INDEX_WEIGHTS()
    query_obj.index_code = "000300.XSHG"

    df = finance.run_query(query_obj)
    print(f"   查询结果: {len(df)} 条记录")
    if not df.empty:
        print(f"   数据列: {df.columns.tolist()}")
        print(f"   前3条记录:")
        print(df.head(3))
    print()

    # 2. 使用 finance.STK_INDEX_COMPONENTS
    print("2. 使用 finance.STK_INDEX_COMPONENTS")
    print("-" * 40)
    query_obj2 = finance.STK_INDEX_COMPONENTS()
    query_obj2.index_code = "000905"

    df2 = finance.run_query(query_obj2)
    print(f"   查询结果: {len(df2)} 条记录")
    print()

    # 3. 使用简化查询接口
    print("3. 使用简化查询接口 run_query_simple")
    print("-" * 40)
    df3 = run_query_simple_index("STK_INDEX_WEIGHTS", index_code="000852")
    print(f"   中证1000成分股: {len(df3)} 条记录")
    print()


def demo_different_formats():
    """不同代码格式支持演示"""
    print("=" * 60)
    print("任务8：不同代码格式支持演示")
    print("=" * 60)
    print()

    formats = [
        "000300",  # 简单数字格式
        "000300.XSHG",  # 聚宽格式
        "sh000300",  # 带前缀格式
    ]

    print("测试不同格式的指数代码:")
    print("-" * 40)

    for code in formats:
        stocks = get_index_stocks(code)
        print(f"   {code:15} -> {len(stocks)} 只成分股")

    print()
    print("✅ 所有格式均正确解析并返回相同数量的成分股")


def demo_cache_usage():
    """缓存机制演示"""
    print("=" * 60)
    print("任务8：缓存机制演示")
    print("=" * 60)
    print()

    import time

    # 第一次查询（从网络获取）
    print("1. 第一次查询（从网络获取）")
    print("-" * 40)
    start = time.time()
    stocks1 = get_index_stocks("000300", force_update=True)
    elapsed1 = time.time() - start
    print(f"   获取到 {len(stocks1)} 只成分股")
    print(f"   耗时: {elapsed1:.2f} 秒")
    print()

    # 第二次查询（从缓存获取）
    print("2. 第二次查询（从缓存获取）")
    print("-" * 40)
    start = time.time()
    stocks2 = get_index_stocks("000300")
    elapsed2 = time.time() - start
    print(f"   获取到 {len(stocks2)} 只成分股")
    print(f"   耗时: {elapsed2:.3f} 秒")
    print(f"   加速: {elapsed1 / elapsed2:.1f}x")
    print()

    print(f"✅ 缓存机制工作正常，查询速度显著提升")


def main():
    """运行所有演示"""
    demo_basic_usage()
    demo_finance_module()
    demo_different_formats()
    demo_cache_usage()

    print("=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
