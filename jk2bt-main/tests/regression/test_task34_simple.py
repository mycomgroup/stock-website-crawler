"""
Task 34: 简单验证脚本
直接测试改进后的接口稳健性
"""

import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src")
)

try:
    from jk2bt.core.strategy_base import (
        RobustResult,
        get_index_stocks_robust,
        get_index_weights_robust,
        get_fundamentals_robust,
        get_history_fundamentals_robust,
        _format_index_code,
        SUPPORTED_INDEXES,
    )

    print("✓ 导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)


def test_index_code_format():
    """测试指数代码格式化"""
    print("\n=== 测试指数代码格式化 ===")

    test_cases = [
        ("000300.XSHG", "000300"),
        ("hs300", "000300"),
        ("沪深300", "000300"),
        ("sh000300", "000300"),
        ("000300", "000300"),
        ("399006.XSHE", "399006"),
        ("cyb", "399006"),
        ("创业板", "399006"),
    ]

    passed = 0
    failed = 0

    for input_code, expected in test_cases:
        result = _format_index_code(input_code)
        if result == expected:
            print(f"  ✓ {input_code} -> {result} (expected: {expected})")
            passed += 1
        else:
            print(f"  ✗ {input_code} -> {result} (expected: {expected})")
            failed += 1

    print(f"\n通过: {passed}/{len(test_cases)}")
    return passed, failed


def test_index_stocks_robust():
    """测试指数成分股稳健接口"""
    print("\n=== 测试指数成分股稳健接口 ===")

    test_cases = [
        ("000300.XSHG", "支持的指数"),
        ("hs300", "别名格式"),
        ("999999", "不支持的指数"),
        ("", "空输入"),
    ]

    passed = 0
    failed = 0

    for code, desc in test_cases:
        try:
            result = get_index_stocks_robust(code)
            if isinstance(result, RobustResult):
                print(
                    f"  ✓ {desc}: success={result.success}, data_len={len(result.data)}, reason={result.reason[:50]}..."
                )
                passed += 1
            else:
                print(f"  ✗ {desc}: 返回类型错误 {type(result)}")
                failed += 1
        except Exception as e:
            print(f"  ✗ {desc}: 异常 {e}")
            failed += 1

    print(f"\n通过: {passed}/{len(test_cases)}")
    return passed, failed


def test_index_weights_robust():
    """测试指数权重稳健接口"""
    print("\n=== 测试指数权重稳健接口 ===")

    test_cases = [
        ("000300.XSHG", "支持的指数"),
        ("000016.XSHG", "上证50"),
        ("999999", "不支持的指数"),
    ]

    passed = 0
    failed = 0

    for code, desc in test_cases:
        try:
            result = get_index_weights_robust(code)
            if isinstance(result, RobustResult):
                print(
                    f"  ✓ {desc}: success={result.success}, df_shape={result.data.shape}, reason={result.reason[:50]}..."
                )
                passed += 1
            else:
                print(f"  ✗ {desc}: 返回类型错误 {type(result)}")
                failed += 1
        except Exception as e:
            print(f"  ✗ {desc}: 异常 {e}")
            failed += 1

    print(f"\n通过: {passed}/{len(test_cases)}")
    return passed, failed


def test_fundamentals_robust():
    """测试基本面查询稳健接口"""
    print("\n=== 测试基本面查询稳健接口 ===")

    from jk2bt.core.strategy_base import query, valuation

    test_cases = [
        (query(valuation), "空symbols"),
        ({"table": "balance", "symbol": []}, "dict格式空symbols"),
        (None, "None查询对象"),
    ]

    passed = 0
    failed = 0

    for query_obj, desc in test_cases:
        try:
            result = get_fundamentals_robust(query_obj)
            if isinstance(result, RobustResult):
                print(
                    f"  ✓ {desc}: success={result.success}, df_empty={result.data.empty}, reason={result.reason[:50]}..."
                )
                passed += 1
            else:
                print(f"  ✗ {desc}: 返回类型错误 {type(result)}")
                failed += 1
        except Exception as e:
            print(f"  ✗ {desc}: 异常 {e}")
            failed += 1

    print(f"\n通过: {passed}/{len(test_cases)}")
    return passed, failed


def test_history_fundamentals_robust():
    """测试历史基本面查询稳健接口"""
    print("\n=== 测试历史基本面查询稳健接口 ===")

    test_cases = [
        (None, ["balance.total_assets"], "空security"),
        ("600519.XSHG", None, "空fields"),
        ("600519.XSHG", ["invalid_field"], "无效字段格式"),
        ("600519.XSHG", ["balance.total_assets"], "有效字段"),
    ]

    passed = 0
    failed = 0

    for security, fields, desc in test_cases:
        try:
            result = get_history_fundamentals_robust(security, fields)
            if isinstance(result, RobustResult):
                print(
                    f"  ✓ {desc}: success={result.success}, df_empty={result.data.empty}, reason={result.reason[:50]}..."
                )
                passed += 1
            else:
                print(f"  ✗ {desc}: 返回类型错误 {type(result)}")
                failed += 1
        except Exception as e:
            print(f"  ✗ {desc}: 异常 {e}")
            failed += 1

    print(f"\n通过: {passed}/{len(test_cases)}")
    return passed, failed


def main():
    print("=" * 60)
    print("Task 34: 指数与基本面接口稳健性验证")
    print("=" * 60)

    total_passed = 0
    total_failed = 0

    p, f = test_index_code_format()
    total_passed += p
    total_failed += f

    p, f = test_index_stocks_robust()
    total_passed += p
    total_failed += f

    p, f = test_index_weights_robust()
    total_passed += p
    total_failed += f

    p, f = test_fundamentals_robust()
    total_passed += p
    total_failed += f

    p, f = test_history_fundamentals_robust()
    total_passed += p
    total_failed += f

    print("\n" + "=" * 60)
    print(f"总计: 通过 {total_passed}/{total_passed + total_failed}")
    print(f"成功率: {total_passed / (total_passed + total_failed) * 100:.1f}%")
    print("=" * 60)

    if total_failed > 0:
        print("\n⚠ 有测试失败，请检查")
        return False
    else:
        print("\n✓ 所有测试通过")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
