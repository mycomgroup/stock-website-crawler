"""
src/data_access/examples/usage_example.py
统一数据访问层使用示例。

演示:
1. 获取数据源
2. 查询各类数据
3. 使用 Mock 数据源测试
4. 自定义数据源注册
"""

import pandas as pd
from datetime import date

# === 示例 1: 获取数据源 ===

def example_get_data_source():
    """
    示例: 获取默认数据源。
    """
    from jk2bt.data_access import get_data_source

    # 获取数据源
    source = get_data_source()

    # 查看数据源信息
    info = source.get_source_info()
    print(f"数据源: {info['name']}")
    print(f"类型: {info['type']}")
    print(f"描述: {info['description']}")

    return source


# === 示例 2: 获取日线数据 ===

def example_get_daily_data():
    """
    示例: 获取股票日线数据。
    """
    from jk2bt.data_access import get_data_source

    source = get_data_source()

    # 获取日线数据
    df = source.get_daily_data(
        symbol="sh600000",       # 浦发银行
        start_date="2020-01-01",
        end_date="2020-12-31",
        adjust="qfq",            # 前复权
    )

    print(f"获取到 {len(df)} 条日线数据")
    print(df.head())

    return df


# === 示例 3: 获取指数成分股 ===

def example_get_index_stocks():
    """
    示例: 获取指数成分股列表。
    """
    from jk2bt.data_access import get_data_source

    source = get_data_source()

    # 获取沪深300成分股
    stocks = source.get_index_stocks("000300.XSHG")
    print(f"沪深300成分股数量: {len(stocks)}")
    print(f"成分股列表: {stocks[:10]}")

    # 获取成分股详情（含权重）
    components = source.get_index_components("000300.XSHG", include_weights=True)
    print(f"成分股详情:")
    print(components.head())

    return stocks


# === 示例 4: 获取交易日 ===

def example_get_trading_days():
    """
    示例: 获取交易日列表。
    """
    from jk2bt.data_access import get_data_source

    source = get_data_source()

    # 获取所有交易日
    all_days = source.get_trading_days()
    print(f"总交易日数量: {len(all_days)}")

    # 获取指定范围的交易日
    days_2020 = source.get_trading_days(
        start_date="2020-01-01",
        end_date="2020-12-31",
    )
    print(f"2020年交易日数量: {len(days_2020)}")

    return days_2020


# === 示例 5: 获取资金流向 ===

def example_get_money_flow():
    """
    示例: 获取资金流向数据。
    """
    from jk2bt.data_access import get_data_source

    source = get_data_source()

    # 获取北向资金流向
    north_flow = source.get_north_money_flow(
        start_date="2020-01-01",
        end_date="2020-03-31",
    )
    print(f"北向资金流向:")
    print(north_flow.head())

    return north_flow


# === 示例 6: 使用 Mock 数据源测试 ===

def example_use_mock_data_source():
    """
    示例: 使用 Mock 数据源进行测试。
    """
    from jk2bt.data_access import MockDataSource, set_data_source, get_data_source

    # 创建 Mock 数据源
    mock = MockDataSource(seed=42, generate_random=True)

    # 注册 Mock 数据源
    set_data_source(mock)

    # 现在所有数据获取都使用 Mock
    source = get_data_source()
    print(f"当前数据源: {source.name}")

    # 获取 Mock 数据
    df = source.get_daily_data("sh600000", "2020-01-01", "2020-01-31")
    print(f"Mock 日线数据:")
    print(df.head())

    # 获取 Mock 指数成分股
    stocks = source.get_index_stocks("000300.XSHG")
    print(f"Mock 成分股: {stocks}")

    # 模拟错误场景
    mock.set_error_mode("network_error")
    try:
        source.get_daily_data("sh600000", "2020-01-01", "2020-01-31")
    except Exception as e:
        print(f"模拟网络错误: {e}")

    # 清除错误模式
    mock.clear_error_mode()

    # 恢复默认数据源
    from jk2bt.data_access import reset_data_source
    reset_data_source()

    print("已恢复默认数据源")


# === 示例 7: 注入预设 Mock 数据 ===

def example_inject_mock_data():
    """
    示例: 注入预设的 Mock 数据。
    """
    from jk2bt.data_access import MockDataSource, set_data_source
    import pandas as pd

    # 创建预设数据
    preset_daily = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"]),
        "open": [10.0, 10.2, 10.5],
        "high": [10.5, 10.5, 11.0],
        "low": [9.8, 10.0, 10.2],
        "close": [10.2, 10.3, 10.8],
        "volume": [1000000, 1100000, 1200000],
    })

    preset_data = {
        "daily": {
            "sh600000": preset_daily,
            "600000.XSHG": preset_daily,
        },
        "trading_days": ["2020-01-02", "2020-01-03", "2020-01-06"],
    }

    # 创建带预设数据的 Mock
    mock = MockDataSource(seed=42, preset_data=preset_data)

    # 注入额外的数据
    another_df = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-02-01", "2020-02-02"]),
        "open": [15.0, 15.5],
        "high": [15.5, 16.0],
        "low": [14.8, 15.2],
        "close": [15.2, 15.8],
        "volume": [800000, 900000],
    })
    mock.set_mock_data("daily", "sz000001", another_df)

    # 注册使用
    set_data_source(mock)

    # 验证预设数据
    df1 = mock.get_daily_data("sh600000", "2020-01-01", "2020-01-10")
    print(f"预设数据 sh600000:")
    print(df1)

    df2 = mock.get_daily_data("sz000001", "2020-02-01", "2020-02-10")
    print(f"注入数据 sz000001:")
    print(df2)

    # 恢复默认
    from jk2bt.data_access import reset_data_source
    reset_data_source()


# === 示例 8: 缓存管理 ===

def example_cache_management():
    """
    示例: 缓存管理。
    """
    from jk2bt.data_access import get_cache, clear_cache

    # 获取缓存管理器
    cache = get_cache()

    # 查看缓存状态
    stats = cache.stats()
    print(f"缓存状态: {stats}")

    # 清空缓存
    clear_cache()
    print("缓存已清空")

    # 再次查看状态
    stats = cache.stats()
    print(f"清空后缓存状态: {stats}")


# === 示例 9: 数据源健康检查 ===

def example_health_check():
    """
    示例: 数据源健康检查。
    """
    from jk2bt.data_access import get_source_health, get_data_source

    # 健康检查
    health = get_source_health()
    print(f"数据源健康状态: {health}")

    # 使用数据源的 health_check 方法
    source = get_data_source()
    health = source.health_check()
    print(f"详细健康信息: {health}")


# === 示例 10: 完整工作流 ===

def example_complete_workflow():
    """
    示例: 完整的数据获取工作流。
    """
    from jk2bt.data_access import get_data_source

    source = get_data_source()

    print("=" * 50)
    print("完整数据获取工作流")
    print("=" * 50)

    # 1. 检查数据源健康
    health = source.health_check()
    print(f"1. 健康检查: {health['status']}")

    # 2. 交易日
    trading_days = source.get_trading_days("2020-01-01", "2020-01-31")
    print(f"2. 交易日数量: {len(trading_days)}")

    # 3. 指数成分股
    stocks = source.get_index_stocks("000300.XSHG")
    print(f"3. 沪深300成分股数量: {len(stocks)}")

    # 4. 成分股日线数据
    if stocks:
        first_stock = stocks[0]
        df = source.get_daily_data(first_stock, "2020-01-01", "2020-01-31")
        print(f"4. {first_stock} 日线数据量: {len(df)}")

    # 5. 北向资金
    north_flow = source.get_north_money_flow("2020-01-01", "2020-01-31")
    print(f"5. 北向资金数据量: {len(north_flow)}")

    print("=" * 50)
    print("工作流完成")
    print("=" * 50)


# === 运行示例 ===

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("统一数据访问层使用示例")
    print("=" * 60 + "\n")

    # 运行示例 (使用 Mock 数据源避免网络请求)
    from jk2bt.data_access import MockDataSource, set_data_source, reset_data_source

    # 设置 Mock 数据源
    mock = MockDataSource(seed=42, generate_random=True)
    set_data_source(mock)

    print("\n[示例 1] 获取数据源")
    example_get_data_source()

    print("\n[示例 2] 获取日线数据")
    example_get_daily_data()

    print("\n[示例 3] 获取指数成分股")
    example_get_index_stocks()

    print("\n[示例 4] 获取交易日")
    example_get_trading_days()

    print("\n[示例 5] 获取资金流向")
    example_get_money_flow()

    print("\n[示例 6] 使用 Mock 数据源")
    example_use_mock_data_source()

    # 恢复 Mock 数据源（因为示例6重置了）
    set_data_source(mock)

    print("\n[示例 7] 注入预设 Mock 数据")
    example_inject_mock_data()

    # 再次设置 Mock
    set_data_source(mock)

    print("\n[示例 8] 缓存管理")
    example_cache_management()

    print("\n[示例 9] 数据源健康检查")
    example_health_check()

    print("\n[示例 10] 完整工作流")
    example_complete_workflow()

    # 恢复默认数据源
    reset_data_source()

    print("\n" + "=" * 60)
    print("所有示例完成")
    print("=" * 60 + "\n")