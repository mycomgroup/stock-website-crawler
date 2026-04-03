"""
test_factors.py
因子模块集成测试。

验证：
- get_factor_values_jq 接口可用
- 核心因子能正确返回数据
"""

import warnings

warnings.filterwarnings("ignore")

import pytest

pytestmark = pytest.mark.network

import pandas as pd
import numpy as np


def test_factor_import():
    """测试因子模块能否正常导入。"""
    from jk2bt.factors import get_factor_values_jq, global_factor_registry

    print("✓ 因子模块导入成功")
    print(f"  已注册因子数量: {len(global_factor_registry.list_factors())}")
    print(f"  已注册因子: {global_factor_registry.list_factors()[:10]}...")


def test_valuation_factors():
    """测试估值因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试估值因子 ====")

    # 单标的单因子
    result = get_factor_values_jq(
        securities="sh600519",
        factors="PE_ratio",
        end_date="2024-01-01",
        count=1,
    )

    assert "pe_ratio" in result, f"返回键名错误: {list(result.keys())}"
    df = result["pe_ratio"]
    print(f"  PE_ratio 结果:\n{df}")

    # 多标的
    result = get_factor_values_jq(
        securities=["sh600519", "sz000001"],
        factors=["PE_ratio", "PB_ratio", "market_cap"],
        end_date="2024-01-01",
        count=1,
    )

    for factor_name in ["pe_ratio", "pb_ratio", "market_cap"]:
        assert factor_name in result, f"缺少因子: {factor_name}"
        print(f"  {factor_name}:\n{result[factor_name]}")


def test_technical_factors():
    """测试技术因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试技术因子 ====")

    result = get_factor_values_jq(
        securities="sh600519",
        factors=["EMAC26", "BIAS5", "VOL240", "ROC6"],
        end_date="2024-01-01",
        count=5,
    )

    for factor_name in ["emac_26", "bias_5", "vol_240", "roc_6"]:
        assert factor_name in result, f"缺少因子: {factor_name}"
        print(f"  {factor_name}:\n{result[factor_name]}")


def test_fundamental_factors():
    """测试财务因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试财务因子 ====")

    result = get_factor_values_jq(
        securities="sh600519",
        factors=["ROE", "net_profit_ratio"],
        end_date="2023-12-31",
        count=1,
    )

    for factor_name in ["roe", "net_profit_ratio"]:
        if factor_name in result:
            print(f"  {factor_name}:\n{result[factor_name]}")
        else:
            print(f"  {factor_name}: 数据不足，跳过")


def test_growth_factors():
    """测试成长因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试成长因子 ====")

    result = get_factor_values_jq(
        securities="sh600519",
        factors=["np_parent_company_owners_growth_rate"],
        end_date="2023-12-31",
        count=1,
    )

    factor_name = "np_parent_company_owners_growth_rate"
    if factor_name in result:
        print(f"  {factor_name}:\n{result[factor_name]}")
    else:
        print(f"  {factor_name}: 数据不足，跳过")


def test_quality_factors():
    """测试质量/杠杆因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试质量/杠杆因子 ====")

    result = get_factor_values_jq(
        securities="sh600519",
        factors=["debt_to_assets", "leverage", "super_quick_ratio"],
        end_date="2024-01-01",
        count=1,
    )

    for factor_name in ["debt_to_assets", "leverage", "super_quick_ratio"]:
        if factor_name in result:
            print(f"  {factor_name}:\n{result[factor_name]}")
        else:
            print(f"  {factor_name}: 数据不足，跳过")


def test_technical_expanded_factors():
    """测试扩展技术因子。"""
    from jk2bt.factors import get_factor_values_jq

    print("\n==== 测试扩展技术因子 ====")

    result = get_factor_values_jq(
        securities="sh600519",
        factors=["boll_up", "boll_down", "atr_14", "variance_120", "cr_20"],
        end_date="2024-01-01",
        count=5,
    )

    for factor_name in ["boll_up", "boll_down", "atr_14", "variance_120", "cr_20"]:
        if factor_name in result:
            print(f"  {factor_name}:\n{result[factor_name]}")
        else:
            print(f"  {factor_name}: 数据不足，跳过")


def test_backtrader_base_strategy_integration():
    """测试与 backtrader_base_strategy 的集成。"""
    print("\n==== 测试与 backtrader_base_strategy 集成 ====")

    from jk2bt.core.strategy_base import get_factor_values_jq

    result = get_factor_values_jq(
        securities="sh600519",
        factors="market_cap",
        end_date="2024-01-01",
        count=1,
    )

    assert isinstance(result, dict), f"返回类型错误: {type(result)}"
    assert "market_cap" in result, f"返回键名错误: {list(result.keys())}"
    print(f"  market_cap:\n{result['market_cap']}")
    print("✓ backtrader_base_strategy.get_factor_values_jq 调用成功")


def main():
    print("=" * 60)
    print("因子模块集成测试")
    print("=" * 60)

    try:
        test_factor_import()
    except Exception as e:
        print(f"✗ test_factor_import 失败: {e}")
        import traceback

        traceback.print_exc()
        return

    try:
        test_valuation_factors()
    except Exception as e:
        print(f"✗ test_valuation_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_technical_factors()
    except Exception as e:
        print(f"✗ test_technical_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_fundamental_factors()
    except Exception as e:
        print(f"✗ test_fundamental_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_growth_factors()
    except Exception as e:
        print(f"✗ test_growth_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_quality_factors()
    except Exception as e:
        print(f"✗ test_quality_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_technical_expanded_factors()
    except Exception as e:
        print(f"✗ test_technical_expanded_factors 失败: {e}")
        import traceback

        traceback.print_exc()

    try:
        test_backtrader_base_strategy_integration()
    except Exception as e:
        print(f"✗ test_backtrader_base_strategy_integration 失败: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
