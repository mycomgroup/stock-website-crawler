#!/usr/bin/env python3
"""
test_strategy_with_cache.py
使用已有缓存数据测试策略运行

测试样本策略，验证系统能否正常运行
"""

import pandas as pd
import backtrader as bt
from datetime import datetime

try:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from market_data.stock import get_stock_daily
except ImportError:
    from .db.duckdb_manager import DuckDBManager
    from .market_data.stock import get_stock_daily

from jk2bt.core.runner import load_jq_strategy, JQStrategyWrapper


def test_simple_strategy():
    """
    测试简单策略 - 使用01_valid_strategy.txt
    """
    print("=" * 80)
    print("测试1: 简单策略加载和运行")
    print("=" * 80)

    strategy_file = "tests/sample_strategies/01_valid_strategy.txt"

    print(f"策略文件: {strategy_file}")

    try:
        functions = load_jq_strategy(strategy_file)
        print(f"✓ 加载成功，函数列表: {list(functions.keys())}")

        if "initialize" not in functions:
            print("✗ 缺少initialize函数")
            return False

        print("✓ 策略结构完整")
        return True

    except Exception as e:
        print(f"✗ 加载失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_with_cached_data():
    """
    使用缓存数据测试策略运行
    """
    print("\n" + "=" * 80)
    print("测试2: 使用缓存数据运行策略")
    print("=" * 80)

    db_path = "data/market.db"

    try:
        conn = DuckDBManager(db_path, read_only=True)

        symbols = conn.execute(
            "SELECT DISTINCT symbol FROM stock_daily ORDER BY symbol LIMIT 5"
        ).fetchdf()
        print(f"可用股票代码样本: {symbols['symbol'].tolist()}")

        start_date = "2020-01-01"
        end_date = "2020-12-31"

        test_symbol = "sh600519"

        print(f"\n尝试获取 {test_symbol} 的数据 ({start_date} ~ {end_date})")

        df = get_stock_daily(test_symbol, start_date, end_date, force_update=False)

        if df.empty:
            print("✗ 无法获取数据")
            return False

        print(f"✓ 获取数据成功，行数: {len(df)}")
        print(f"数据列: {df.columns.tolist()}")
        print(f"日期范围: {df['datetime'].min()} ~ {df['datetime'].max()}")

        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name=test_symbol,
        )

        print(f"✓ 创建Backtrader数据feed成功")

        return True

    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_strategy_execution():
    """
    测试策略实际执行
    """
    print("\n" + "=" * 80)
    print("测试3: 策略实际执行（短周期）")
    print("=" * 80)

    strategy_file = "tests/sample_strategies/01_valid_strategy.txt"

    start_date = "2020-01-01"
    end_date = "2020-03-31"
    initial_capital = 100000

    try:
        print("加载策略...")
        functions = load_jq_strategy(strategy_file)
        print(f"✓ 加载成功: {list(functions.keys())}")

        print("获取数据...")
        test_symbol = "sh600519"
        df = get_stock_daily(test_symbol, start_date, end_date, force_update=False)

        if df.empty:
            print("✗ 数据为空")
            return False

        print(f"✓ 数据获取成功: {len(df)} 行")

        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name=test_symbol,
        )

        print("创建Cerebro引擎...")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initial_capital)
        cerebro.broker.setcommission(commission=0.0002)
        cerebro.adddata(data)

        print("添加策略...")
        cerebro.addstrategy(JQStrategyWrapper, strategy_functions=functions)

        print(f"开始回测...")
        print(f"初始资金: {initial_capital:,.2f}")
        print(f"日期范围: {start_date} ~ {end_date}")

        results = cerebro.run()

        final_value = cerebro.broker.getvalue()
        pnl = final_value - initial_capital
        pnl_pct = (final_value / initial_capital - 1) * 100

        print(f"\n✓ 回测完成!")
        print(f"最终资金: {final_value:,.2f}")
        print(f"盈亏: {pnl:,.2f} ({pnl_pct:.2f}%)")

        strategy = results[0]

        if hasattr(strategy, "navs") and strategy.navs:
            nav_series = pd.Series(strategy.navs)
            cummax = nav_series.cummax()
            drawdown = (nav_series - cummax) / cummax
            max_dd = drawdown.min()
            print(f"最大回撤: {max_dd:.2%}")

            days = len(nav_series)
            annual_return = (final_value / initial_capital) ** (252 / days) - 1
            print(f"年化收益: {annual_return:.2%}")

        return True

    except Exception as e:
        print(f"✗ 执行失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("\n开始测试策略系统...")

    results = []

    results.append(("策略加载测试", test_simple_strategy()))
    results.append(("缓存数据测试", test_with_cached_data()))
    results.append(("策略执行测试", test_strategy_execution()))

    print("\n" + "=" * 80)
    print("测试总结:")
    print("=" * 80)

    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")

    all_passed = all(r[1] for r in results)

    print("\n总体状态:", "✓ 所有测试通过" if all_passed else "✗ 存在失败测试")

    return all_passed


if __name__ == "__main__":
    main()
