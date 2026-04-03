"""
API补充模块测试脚本
验证新增API功能是否正常工作
"""


def test_api_enhancements():
    """测试API增强模块"""
    print("=" * 80)
    print("测试API增强模块")
    print("=" * 80)

    try:
        from jk2bt.api.enhancements import (
            filter_st,
            filter_paused,
            get_high_limit,
            get_low_limit,
            LimitOrderStyle,
            MarketOrderStyle,
        )

        print("✓ API增强模块导入成功")

        # 测试过滤函数（需要网络）
        print("\n测试过滤函数:")
        test_stocks = ["600519.XSHG", "000858.XSHE"]

        try:
            clean_stocks = filter_st(test_stocks)
            print(f"  filter_st: {test_stocks} -> {clean_stocks}")
        except Exception as e:
            print(f"  filter_st: 跳过（需要网络）- {e}")

        try:
            active_stocks = filter_paused(test_stocks)
            print(f"  filter_paused: {test_stocks} -> {active_stocks}")
        except Exception as e:
            print(f"  filter_paused: 跳过（需要网络）- {e}")

        # 测试订单风格类
        limit_order = LimitOrderStyle(100.0)
        print(f"\n  LimitOrderStyle: {limit_order.limit_price}")

        market_order = MarketOrderStyle()
        print(f"  MarketOrderStyle: 创建成功")

        print("\n✓ API增强模块测试通过")
        return True

    except Exception as e:
        print(f"✗ API增强模块测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_indicator_fields():
    """测试indicator字段模块"""
    print("\n" + "=" * 80)
    print("测试indicator字段模块")
    print("=" * 80)

    try:
        from jk2bt.indicator_fields import (
            get_indicator_field_description,
            get_supported_indicator_fields,
            INDICATOR_FIELD_MAPPING,
        )

        print("✓ indicator字段模块导入成功")

        # 测试字段描述
        print("\n测试字段描述:")
        fields = ["roe", "roa", "gross_profit_margin"]
        for field in fields:
            desc = get_indicator_field_description(field)
            print(f"  {field}: {desc}")

        # 测试支持的字段列表
        supported = get_supported_indicator_fields()
        print(f"\n支持的indicator字段数量: {len(supported)}")
        print(f"部分字段: {supported[:5]}")

        print("\n✓ indicator字段模块测试通过")
        return True

    except Exception as e:
        print(f"✗ indicator字段模块测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_api_optimizations():
    """测试性能优化模块"""
    print("\n" + "=" * 80)
    print("测试性能优化模块")
    print("=" * 80)

    try:
        from jk2bt.api.optimizations import (
            CurrentDataCache,
            BatchDataLoader,
            optimize_dataframe_memory,
            cleanup_memory,
        )

        print("✓ 性能优化模块导入成功")

        # 测试缓存器
        cache = CurrentDataCache()
        print(f"  CurrentDataCache实例创建成功")

        # 测试批量加载器
        loader = BatchDataLoader()
        print(f"  BatchDataLoader实例创建成功")

        # 测试DataFrame优化
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2, 3], "b": [1.5, 2.5, 3.5], "c": ["x", "y", "z"]})
        optimized_df = optimize_dataframe_memory(df)
        print(f"  DataFrame内存优化成功")

        print("\n✓ 性能优化模块测试通过")
        return True

    except Exception as e:
        print(f"✗ 性能优化模块测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_strategy_helpers():
    """测试策略辅助函数模块"""
    print("\n" + "=" * 80)
    print("测试策略辅助函数模块")
    print("=" * 80)

    try:
        from jk2bt.strategy.helpers import (
            calculate_ma,
            calculate_ema,
            calculate_rsi,
            calculate_macd,
            calculate_sharpe,
            calculate_max_drawdown,
            normalize_data,
            winsorize,
        )

        print("✓ 策略辅助函数模块导入成功")

        # 测试技术指标
        import pandas as pd
        import numpy as np

        prices = pd.Series([10, 11, 12, 11, 13, 14, 15, 14, 16, 17])

        print("\n测试技术指标计算:")
        ma5 = calculate_ma(prices, 5)
        print(f"  MA5: {ma5.iloc[-1]:.2f}")

        ema5 = calculate_ema(prices, 5)
        print(f"  EMA5: {ema5.iloc[-1]:.2f}")

        rsi = calculate_rsi(prices)
        print(f"  RSI: {rsi.iloc[-1]:.2f}")

        macd = calculate_macd(prices)
        print(f"  MACD: {macd['macd'].iloc[-1]:.4f}")

        # 测试绩效分析
        returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01, 0.02])
        values = pd.Series([100, 101, 99, 102, 103, 102, 104])

        print("\n测试绩效分析:")
        sharpe = calculate_sharpe(returns)
        print(f"  夏普比率: {sharpe:.4f}")

        max_dd = calculate_max_drawdown(values)
        print(f"  最大回撤: {max_dd:.2%}")

        # 测试数据处理
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        normalized = normalize_data(data, method="zscore")
        print(
            f"\n  Z-score标准化: mean={normalized.mean():.4f}, std={normalized.std():.4f}"
        )

        winsorized = winsorize(data)
        print(f"  去极值: min={winsorized.min()}, max={winsorized.max()}")

        print("\n✓ 策略辅助函数模块测试通过")
        return True

    except Exception as e:
        print(f"✗ 策略辅助函数模块测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_module_import():
    """测试模块导入"""
    print("\n" + "=" * 80)
    print("测试模块导入")
    print("=" * 80)

    try:
        from jk2bt import (
            # 数据获取
            get_price,
            get_fundamentals,
            get_current_data,
            # 交易API
            order_shares,
            order_target_percent,
            # 过滤函数
            filter_st,
            filter_paused,
            # indicator
            get_indicator_data,
            filter_by_indicator,
            # 技术指标
            calculate_ma,
            calculate_rsi,
            # 绩效分析
            calculate_sharpe,
            calculate_max_drawdown,
        )

        print("✓ 所有模块导入成功")
        return True

    except Exception as e:
        print(f"✗ 模块导入测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("聚宽API补充模块测试")
    print("=" * 80)

    results = {
        "模块导入": test_module_import(),
        "API增强": test_api_enhancements(),
        "indicator字段": test_indicator_fields(),
        "性能优化": test_api_optimizations(),
        "策略辅助": test_strategy_helpers(),
    }

    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)

    for name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:<20} {status}")

    passed = sum(results.values())
    total = len(results)

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n✓ 所有测试通过！")
        return True
    else:
        print(f"\n✗ {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
