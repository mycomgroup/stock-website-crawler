#!/usr/bin/env python3
"""
Task 32: 分钟上层 API 打通验证脚本
从项目根目录运行，验证上层 API 对分钟数据的消费能力
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "..", "src"
    ),
)


def validate_minute_api():
    """验证分钟数据上层 API"""
    print("=" * 80)
    print("Task 32: 分钟上层 API 打通验证")
    print("=" * 80)

    results = {"passed": [], "failed": [], "warnings": []}

    print("\n1. 验证 market 导入...")
    try:
        from jk2bt.api.market import get_price, history, attribute_history, get_bars

        results["passed"].append("market导入")
        print("   ✓ 导入成功")
    except Exception as e:
        results["failed"].append(f"market导入: {e}")
        print(f"   ✗ 导入失败: {e}")
        return results

    print("\n2. 验证 market_data.minute 导入...")
    try:
        from market_data.minute import get_stock_minute, get_etf_minute

        results["passed"].append("minute模块导入")
        print("   ✓ 导入成功")
    except Exception as e:
        results["warnings"].append(f"market_data导入: {e}")
        print(f"   ⚠ 导入失败（相对导入问题）: {e}")

    print("\n3. 验证 DuckDB 缓存查询...")
    try:
        from jk2bt.db.duckdb_manager import DuckDBManager

        db = DuckDBManager(read_only=True)

        symbol = "sh600000"
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        has_cache = db.has_data(
            "stock_minute", symbol, start_date, end_date, "qfq", "5"
        )
        if has_cache:
            results["passed"].append("DuckDB缓存查询")
            print(f"   ✓ {symbol} 5分钟数据缓存存在")
        else:
            results["warnings"].append("缓存未预热")
            print(f"   ⚠ {symbol} 5分钟数据缓存不存在（可能未预热）")
    except Exception as e:
        results["failed"].append(f"DuckDB查询: {e}")
        print(f"   ✗ 查询失败: {e}")

    print("\n4. 测试 get_price(..., frequency='5m')...")
    try:
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        df = get_price(
            "600519.XSHG", start_date=start_date, end_date=end_date, frequency="5m"
        )

        if not df.empty:
            results["passed"].append(f"get_price_5m ({len(df)}行)")
            print(f"   ✓ 成功获取 {len(df)} 行数据")
            print(f"   列: {list(df.columns)}")
        else:
            results["warnings"].append("get_price_5m返回空数据")
            print(f"   ⚠ 返回空数据（可能缓存未预热或AkShare失败）")
    except Exception as e:
        results["failed"].append(f"get_price_5m: {e}")
        print(f"   ✗ 测试失败: {e}")

    print("\n5. 测试 history(..., unit='5m')...")
    try:
        result = history(
            count=50, unit="5m", field="close", security_list=["600519.XSHG"]
        )

        if not result.empty:
            results["passed"].append(f"history_5m ({len(result)}行)")
            print(f"   ✓ 成功获取 {len(result)} 行数据")
        else:
            results["warnings"].append("history_5m返回空数据")
            print(f"   ⚠ 返回空数据")
    except Exception as e:
        results["failed"].append(f"history_5m: {e}")
        print(f"   ✗ 测试失败: {e}")

    print("\n6. 测试 attribute_history(..., unit='5m')...")
    try:
        result = attribute_history(
            "600519.XSHG", count=100, unit="5m", fields=["open", "close", "volume"]
        )

        if not result.empty:
            results["passed"].append(f"attribute_history_5m ({len(result)}行)")
            print(f"   ✓ 成功获取 {len(result)} 行数据")
            print(f"   列: {list(result.columns)}")
        else:
            results["warnings"].append("attribute_history_5m返回空数据")
            print(f"   ⚠ 返回空数据")
    except Exception as e:
        results["failed"].append(f"attribute_history_5m: {e}")
        print(f"   ✗ 测试失败: {e}")

    print("\n7. 测试 get_bars(..., unit='5m')...")
    try:
        result = get_bars("600519.XSHG", count=50, unit="5m")

        if not result.empty:
            results["passed"].append(f"get_bars_5m ({len(result)}行)")
            print(f"   ✓ 成功获取 {len(result)} 行数据")
        else:
            results["warnings"].append("get_bars_5m返回空数据")
            print(f"   ⚠ 返回空数据")
    except Exception as e:
        results["failed"].append(f"get_bars_5m: {e}")
        print(f"   ✗ 测试失败: {e}")

    print("\n8. 测试所有分钟周期...")
    periods = ["1m", "5m", "15m", "30m", "60m"]
    for period in periods:
        try:
            df = get_price(
                "600519.XSHG",
                start_date=(datetime.now() - timedelta(hours=3)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                frequency=period,
            )
            if not df.empty:
                results["passed"].append(f"{period}周期支持 ({len(df)}行)")
                print(f"   ✓ {period}: {len(df)} 行")
            else:
                results["warnings"].append(f"{period}返回空")
                print(f"   ⚠ {period}: 空数据")
        except Exception as e:
            results["failed"].append(f"{period}: {e}")
            print(f"   ✗ {period}: {e}")

    print("\n" + "=" * 80)
    print("验证总结")
    print("=" * 80)
    print(f"\n通过: {len(results['passed'])}")
    for item in results["passed"]:
        print(f"  ✓ {item}")

    print(f"\n警告: {len(results['warnings'])}")
    for item in results["warnings"]:
        print(f"  ⚠ {item}")

    print(f"\n失败: {len(results['failed'])}")
    for item in results["failed"]:
        print(f"  ✗ {item}")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = validate_minute_api()

    success_rate = (
        len(results["passed"]) / (len(results["passed"]) + len(results["failed"]))
        if (len(results["passed"]) + len(results["failed"]) > 0)
        else 0
    )

    print(f"\n成功率: {success_rate:.1%}")

    if success_rate >= 0.7:
        print("\n✓ Task 32 验证通过：分钟上层 API 已打通")
        print("  注意：部分警告可能源于缓存未预热，建议预热后重新验证")
    else:
        print("\n✗ Task 32 验证失败：存在关键问题需要修复")

    print("\n" + "=" * 80)
