#!/usr/bin/env python3
"""
测试 get_money_flow 功能
验证返回结果可直接筛选、排序、取列
"""

from market_data import get_money_flow
import pandas as pd


def test_basic_usage():
    """基础用法测试"""
    print("=" * 50)
    print("测试 1: 基础用法 - 单只股票")
    print("=" * 50)
    df = get_money_flow(
        "sh600519", count=5, fields=["sec_code", "date", "change_pct", "net_pct_main"]
    )
    print(df)
    assert not df.empty, "数据不应为空"
    assert "sec_code" in df.columns, "应包含 sec_code 列"
    assert "change_pct" in df.columns, "应包含 change_pct 列"
    print("✓ 通过\n")


def test_multiple_stocks():
    """多只股票测试"""
    print("=" * 50)
    print("测试 2: 多只股票")
    print("=" * 50)
    stocks = ["sh600519", "sz000001", "sz000002"]
    df = get_money_flow(stocks, count=3, fields=["sec_code", "date", "change_pct"])
    print(df)
    assert len(df["sec_code"].unique()) == 3, "应包含 3 只股票的数据"
    print("✓ 通过\n")


def test_positional_args():
    """位置参数测试（兼容策略调用方式）"""
    print("=" * 50)
    print("测试 3: 位置参数调用（兼容策略）")
    print("=" * 50)
    # 模拟策略: get_money_flow(stocks, None, date, fields, count)
    df = get_money_flow("sh600519", None, "2025-09-25", ["sec_code", "change_pct"], 1)
    print(df)
    assert not df.empty, "数据不应为空"
    print("✓ 通过\n")


def test_keyword_args():
    """关键字参数测试"""
    print("=" * 50)
    print("测试 4: 关键字参数调用")
    print("=" * 50)
    df = get_money_flow(
        security_list="sh600519",
        end_date="2025-09-25",
        fields=["sec_code", "net_pct_main"],
        count=1,
    )
    print(df)
    assert not df.empty, "数据不应为空"
    print("✓ 通过\n")


def test_filtering():
    """筛选测试"""
    print("=" * 50)
    print("测试 5: 数据筛选（涨幅 < 0）")
    print("=" * 50)
    df = get_money_flow(
        ["sh600519", "sz000001"], count=1, fields=["sec_code", "change_pct"]
    )
    filtered = df[df["change_pct"] < 0]
    print("原始数据:")
    print(df)
    print("\n筛选后 (change_pct < 0):")
    print(filtered)
    print("✓ 通过\n")


def test_pivot():
    """Pivot 测试"""
    print("=" * 50)
    print("测试 6: Pivot 操作")
    print("=" * 50)
    df = get_money_flow(
        ["sh600519", "sz000001"], count=2, fields=["sec_code", "date", "change_pct"]
    )
    pivot_df = df.pivot(index="sec_code", columns="date", values="change_pct")
    print("原始数据:")
    print(df)
    print("\nPivot 结果:")
    print(pivot_df)
    assert pivot_df.shape[0] == 2, "应有 2 只股票"
    print("✓ 通过\n")


def test_groupby():
    """分组聚合测试"""
    print("=" * 50)
    print("测试 7: 分组聚合")
    print("=" * 50)
    df = get_money_flow(
        ["sh600519", "sz000001"],
        count=5,
        fields=["sec_code", "net_amount_xl", "net_amount_l"],
    )
    grouped = df.groupby("sec_code").sum()
    print("原始数据:")
    print(df)
    print("\n分组求和:")
    print(grouped)
    assert len(grouped) == 2, "应有 2 只股票"
    print("✓ 通过\n")


def test_all_fields():
    """所有字段测试"""
    print("=" * 50)
    print("测试 8: 所有字段")
    print("=" * 50)
    df = get_money_flow("sh600519", count=1)
    print("字段列表:")
    print(df.columns.tolist())
    print("\n数据:")
    print(df)
    assert "sec_code" in df.columns, "应包含 sec_code"
    assert "date" in df.columns, "应包含 date"
    assert "change_pct" in df.columns, "应包含 change_pct"
    assert "net_pct_main" in df.columns, "应包含 net_pct_main"
    print("✓ 通过\n")


def test_symbol_formats():
    """股票代码格式测试"""
    print("=" * 50)
    print("测试 9: 不同股票代码格式")
    print("=" * 50)
    # 测试 XSHG/XSHE 格式
    df1 = get_money_flow("600519.XSHG", count=1, fields=["sec_code", "change_pct"])
    print("600519.XSHG 格式:")
    print(df1)

    # 测试纯数字格式
    df2 = get_money_flow("000001", count=1, fields=["sec_code", "change_pct"])
    print("\n000001 格式:")
    print(df2)

    # 测试 sh/sz 前缀格式
    df3 = get_money_flow("sh600519", count=1, fields=["sec_code", "change_pct"])
    print("\nsh600519 格式:")
    print(df3)

    assert not df1.empty, "XSHG 格式应返回数据"
    assert not df2.empty, "纯数字格式应返回数据"
    assert not df3.empty, "sh 前缀格式应返回数据"
    print("✓ 通过\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("开始测试 get_money_flow 功能")
    print("=" * 50 + "\n")

    test_basic_usage()
    test_multiple_stocks()
    test_positional_args()
    test_keyword_args()
    test_filtering()
    test_pivot()
    test_groupby()
    test_all_fields()
    test_symbol_formats()

    print("=" * 50)
    print("所有测试通过！✓")
    print("=" * 50)
