#!/usr/bin/env python3
"""
download_common_stocks.py
下载常用股票数据到本地缓存（2020-2023）

用途：
- 预热本地数据缓存
- 支持离线模式运行策略
- 提高回测速度

使用方法：
    python download_common_stocks.py --start 2020-01-01 --end 2023-12-31 --sample
    python download_common_stocks.py --full  # 下载沪深300+中证500成分股
"""

import sys
import os
import time
import argparse
from datetime import datetime

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src")
)

try:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from market_data.stock import get_stock_daily
    from market_data.index import get_index_daily
    from utils.symbol import format_stock_symbol
except ImportError:
    print("导入模块失败，请确保在项目根目录运行")
    sys.exit(1)


def get_sample_stocks():
    """
    获取示例股票池（用于快速测试）

    返回: 常用蓝筹股列表
    """
    return [
        "sh600519",  # 贵州茅台
        "sz000858",  # 五粮液
        "sz000333",  # 美的集团
        "sh600036",  # 招商银行
        "sh601318",  # 中国平安
        "sz000001",  # 平安银行
        "sh601166",  # 兴业银行
        "sh600000",  # 浦发银行
        "sz000002",  # 万科A
        "sh600276",  # 恒瑞医药
        "sz000568",  # 泸州老窖
        "sh601398",  # 工商银行
        "sh601288",  # 农业银行
        "sh601939",  # 建设银行
        "sh601988",  # 中国银行
    ]


def get_hs300_stocks():
    """
    获取沪深300成分股代码

    返回: 股票代码列表
    """
    try:
        import akshare as ak

        print("获取沪深300成分股...")
        df = ak.index_stock_cons_weight_csindex(symbol="000300")

        if df is None or df.empty:
            print("警告: 无法获取沪深300成分股，使用示例股票")
            return get_sample_stocks()

        stocks = []
        for code in df["成分券代码"].values:
            code = str(code).zfill(6)
            if code.startswith("6"):
                stocks.append(f"sh{code}")
            else:
                stocks.append(f"sz{code}")

        return stocks[:50]  # 限制前50只

    except Exception as e:
        print(f"获取沪深300成分股失败: {e}")
        return get_sample_stocks()


def get_zz500_stocks():
    """
    获取中证500成分股代码

    返回: 股票代码列表
    """
    try:
        import akshare as ak

        print("获取中证500成分股...")
        df = ak.index_stock_cons_weight_csindex(symbol="000905")

        if df is None or df.empty:
            print("警告: 无法获取中证500成分股")
            return []

        stocks = []
        for code in df["成分券代码"].values:
            code = str(code).zfill(6)
            if code.startswith("6"):
                stocks.append(f"sh{code}")
            else:
                stocks.append(f"sz{code}")

        return stocks[:50]  # 限制前50只

    except Exception as e:
        print(f"获取中证500成分股失败: {e}")
        return []


def download_stocks(stocks, start_date, end_date, adjust="qfq", batch_size=10, delay=1):
    """
    批量下载股票数据

    参数:
        stocks: 股票代码列表
        start_date: 起始日期
        end_date: 结束日期
        adjust: 复权方式
        batch_size: 批次大小
        delay: 批次间延迟（秒）
    """
    total = len(stocks)
    success_count = 0
    failed_stocks = []

    print(f"\n开始下载 {total} 只股票数据...")
    print(f"日期范围: {start_date} ~ {end_date}")
    print(f"复权方式: {adjust}")
    print("=" * 80)

    for i in range(0, total, batch_size):
        batch = stocks[i : i + batch_size]

        print(f"\n批次 {i // batch_size + 1}/{(total - 1) // batch_size + 1}:")

        for j, stock in enumerate(batch, 1):
            try:
                print(f"  [{i + j}/{total}] {stock}...", end="", flush=True)

                df = get_stock_daily(
                    stock, start_date, end_date, force_update=True, adjust=adjust
                )

                if df is not None and not df.empty:
                    print(f" ✓ ({len(df)}行)")
                    success_count += 1
                else:
                    print(" ✗ (空数据)")
                    failed_stocks.append(stock)

            except Exception as e:
                print(f" ✗ ({e})")
                failed_stocks.append(stock)

        if i + batch_size < total and delay > 0:
            print(f"  等待 {delay} 秒...")
            time.sleep(delay)

    print("\n" + "=" * 80)
    print(f"下载完成:")
    print(f"  成功: {success_count}/{total}")
    print(f"  失败: {len(failed_stocks)}/{total}")

    if failed_stocks:
        print(
            f"\n失败股票: {failed_stocks[:10]}{'...' if len(failed_stocks) > 10 else ''}"
        )

    return success_count, failed_stocks


def download_indexes(start_date, end_date):
    """
    下载常用指数数据

    参数:
        start_date: 起始日期
        end_date: 结束日期
    """
    indexes = [
        ("sh000300", "沪深300"),
        ("sh000905", "中证500"),
        ("sh000852", "中证1000"),
        ("sh000016", "上证50"),
        ("sz399006", "创业板指"),
    ]

    print("\n下载指数数据...")
    print("=" * 80)

    for code, name in indexes:
        try:
            print(f"  {code} ({name})...", end="", flush=True)

            df = get_index_daily(code, start_date, end_date, force_update=True)

            if df is not None and not df.empty:
                print(f" ✓ ({len(df)}行)")
            else:
                print(" ✗ (空数据)")

        except Exception as e:
            print(f" ✗ ({e})")


def main():
    parser = argparse.ArgumentParser(description="下载常用股票数据到本地缓存")
    parser.add_argument(
        "--start", default="2020-01-01", help="起始日期 (默认: 2020-01-01)"
    )
    parser.add_argument(
        "--end", default="2023-12-31", help="结束日期 (默认: 2023-12-31)"
    )
    parser.add_argument(
        "--sample", action="store_true", help="下载示例股票（15只蓝筹股）"
    )
    parser.add_argument(
        "--full", action="store_true", help="下载沪深300+中证500成分股（前50只）"
    )
    parser.add_argument(
        "--adjust",
        default="qfq",
        choices=["qfq", "hfq", ""],
        help="复权方式 (默认: qfq)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=10, help="批次大小 (默认: 10)"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0, help="批次间延迟/秒 (默认: 1.0)"
    )
    parser.add_argument("--skip-indexes", action="store_true", help="跳过指数下载")

    args = parser.parse_args()

    print("=" * 80)
    print("数据预热脚本 - download_common_stocks.py")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.sample:
        stocks = get_sample_stocks()
        print(f"\n模式: 示例股票 ({len(stocks)}只)")
    elif args.full:
        stocks = get_hs300_stocks() + get_zz500_stocks()
        print(f"\n模式: 完整股票池 ({len(stocks)}只)")
    else:
        stocks = get_sample_stocks()
        print(f"\n模式: 默认示例股票 ({len(stocks)}只)")

    if not args.skip_indexes:
        download_indexes(args.start, args.end)

    success, failed = download_stocks(
        stocks,
        args.start,
        args.end,
        adjust=args.adjust,
        batch_size=args.batch_size,
        delay=args.delay,
    )

    print("\n" + "=" * 80)
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    print("\n下一步:")
    print('  1. 检查数据: sqlite3 data/market.db "SELECT COUNT(*) FROM stock_daily"')
    print("  2. 运行离线模式: python run_daily_strategy_batch.py --use-cache-only")
    print("  3. 测试策略: python test_strategy_with_cache.py")


if __name__ == "__main__":
    main()
