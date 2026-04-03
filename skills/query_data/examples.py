#!/usr/bin/env python3
"""
Query Data Plugin 使用示例

演示如何使用各数据源查询股票数据
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_datasource import (
    test_finnhub,
    test_fmp,
    test_alphavantage,
    test_tiingo,
    test_lixinger,
    TestError,
)


def test_us_stocks(symbol="AAPL"):
    """测试美股数据源"""
    print(f"\n{'=' * 60}")
    print(f"测试美股数据源: {symbol}")
    print("=" * 60)

    tests = [
        ("Finnhub", test_finnhub),
        ("FMP", test_fmp),
        ("Alpha Vantage", test_alphavantage),
        ("Tiingo", test_tiingo),
    ]

    for name, test_fn in tests:
        try:
            provider, data = test_fn(symbol)
            print(f"✓ {name}: 连接成功")
            if isinstance(data, dict):
                print(f"  数据预览: {str(data)[:100]}...")
        except TestError as e:
            print(f"✗ {name}: {e}")
        except Exception as e:
            print(f"✗ {name}: 错误 - {e}")


def test_cn_stocks():
    """测试A股数据源（理杏仁）"""
    print(f"\n{'=' * 60}")
    print("测试A股数据源: 理杏仁 (Lixinger)")
    print("=" * 60)

    try:
        provider, data = test_lixinger()
        print(f"✓ 理杏仁: 连接成功")
        print(f"  数据: {data}")
    except TestError as e:
        print(f"✗ 理杏仁: {e}")
        print("  提示: 请设置 LIXINGER_TOKEN 环境变量")
    except Exception as e:
        print(f"✗ 理杏仁: 错误 - {e}")


def main():
    print("\n" + "=" * 60)
    print("Query Data Plugin 使用示例")
    print("=" * 60)

    # 测试美股
    test_us_stocks("AAPL")
    test_us_stocks("MSFT")

    # 测试A股
    test_cn_stocks()

    print(f"\n{'=' * 60}")
    print("测试完成")
    print("=" * 60)
    print("\n使用说明:")
    print("1. 设置环境变量: export API_KEY=xxx")
    print("2. 运行测试: python3 test_datasource.py")
    print("3. 查看文档: README.md")


if __name__ == "__main__":
    main()
