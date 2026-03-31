"""
简单回测示例 - RiceQuant Notebook

验证 notebook 连接和基本 API
"""

print("=== RiceQuant Notebook 简单回测测试 ===")
from datetime import datetime

print(f"当前时间: {datetime.now()}")

try:
    all_stocks = get_all_securities(["stock"])
    print(f"股票总数: {len(all_stocks)}")

    hs300 = index_components("000300.XSHG")
    print(f"沪深300成分股: {len(hs300)}")

    zz500 = index_components("000905.XSHG")
    print(f"中证500成分股: {len(zz500)}")

    dates = get_trading_dates("2024-01-01", "2024-12-31")
    print(f"2024年交易日: {len(dates)}")

    print("\nAPI 测试成功!")

except Exception as e:
    print(f"API 测试错误: {e}")
    print("可能需要在 RiceQuant Notebook 平台上运行")

print("\n=== 测试完成 ===")
