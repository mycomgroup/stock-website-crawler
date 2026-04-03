"""
test_company_info_demo.py
验证上市公司基本信息与状态变动 API 实际功能
"""

from jk2bt.finance_data.company_info import (
    get_company_info,
    get_security_status,
    query_company_basic_info,
    query_status_change,
)
from jk2bt.core.strategy_base import finance, query
import pandas as pd


def test_basic_query():
    print("=" * 60)
    print("测试 1: 查询茅台公司基本信息")
    print("=" * 60)

    symbol = "600519.XSHG"
    df = get_company_info(symbol, use_duckdb=False, force_update=True)
    print(f"茅台公司信息:\n{df}\n")

    if not df.empty:
        print("字段检查:")
        print(f"  - code: {df.iloc[0]['code']}")
        if "company_name" in df.columns:
            print(f"  - company_name: {df.iloc[0]['company_name']}")
        if "industry" in df.columns:
            print(f"  - industry: {df.iloc[0]['industry']}")
        if "list_date" in df.columns:
            print(f"  - list_date: {df.iloc[0]['list_date']}")


def test_multiple_symbols():
    print("\n" + "=" * 60)
    print("测试 2: 查询多家公司基本信息")
    print("=" * 60)

    symbols = ["600519.XSHG", "000001.XSHE", "000858.XSHE"]
    df = query_company_basic_info(symbols)
    print(f"查询结果:\n{df}\n")

    if not df.empty:
        print(f"共查询到 {len(df)} 条记录")


def test_finance_run_query():
    print("\n" + "=" * 60)
    print("测试 3: 使用 finance.run_query 查询")
    print("=" * 60)

    stocks = ["600519.XSHG", "000001.XSHE"]

    df = finance.run_query(
        query(
            finance.STK_COMPANY_BASIC_INFO.code,
            finance.STK_COMPANY_BASIC_INFO.company_name,
            finance.STK_COMPANY_BASIC_INFO.industry,
        ).filter(finance.STK_COMPANY_BASIC_INFO.code.in_(stocks))
    )

    print(f"finance.run_query 结果:\n{df}\n")


def test_security_status():
    print("\n" + "=" * 60)
    print("测试 4: 查询证券状态")
    print("=" * 60)

    symbol = "600519.XSHG"
    df = get_security_status(symbol, use_duckdb=False)
    print(f"茅台证券状态:\n{df}\n")

    if not df.empty:
        print(f"状态类型: {df.iloc[0]['status_type']}")


def test_status_change_with_date():
    print("\n" + "=" * 60)
    print("测试 5: 查询状态变更（带日期范围）")
    print("=" * 60)

    symbols = ["600519.XSHG"]
    start_date = "2025-03-01"
    end_date = "2025-03-28"

    df = query_status_change(symbols, start_date=start_date, end_date=end_date)
    print(f"状态变更查询结果:\n{df}\n")


def test_finance_status_change():
    print("\n" + "=" * 60)
    print("测试 6: 使用 finance.run_query 查询状态变更")
    print("=" * 60)

    stocks = ["600519.XSHG"]

    df = finance.run_query(
        query(
            finance.STK_STATUS_CHANGE.code,
            finance.STK_STATUS_CHANGE.status_type,
        ).filter(finance.STK_STATUS_CHANGE.code.in_(stocks))
    )

    print(f"finance.run_query 状态变更结果:\n{df}\n")


if __name__ == "__main__":
    test_basic_query()
    test_multiple_symbols()
    test_finance_run_query()
    test_security_status()
    test_status_change_with_date()
    test_finance_status_change()

    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
