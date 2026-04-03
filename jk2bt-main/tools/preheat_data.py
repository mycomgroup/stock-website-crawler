#!/usr/bin/env python3
"""
数据预热脚本

在运行策略前，预先下载并缓存常用数据：
- 常用ETF日线数据
- 常用指数日线数据
- 默认股票池数据

使用方法:
    python scripts/preheat_data.py
    python scripts/preheat_data.py --etfs-only
    python scripts/preheat_data.py --start 2022-01-01 --end 2023-12-31
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# 常用ETF列表
COMMON_ETFS = {
    # 沪市ETF
    "510500.XSHG": "中证500ETF",
    "510300.XSHG": "沪深300ETF",
    "510050.XSHG": "上证50ETF",
    "512900.XSHG": "证券ETF",
    "512880.XSHG": "证券ETF(证券公司)",
    "518880.XSHG": "黄金ETF",
    "513100.XSHG": "纳指ETF",
    "510880.XSHG": "红利ETF",
    "511010.XSHG": "国债ETF",
    # 深市ETF
    "159915.XSHE": "创业板ETF",
    "159919.XSHE": "沪深300ETF",
    "159949.XSHE": "创业板50ETF",
    "159941.XSHE": "纳指ETF",
}

# 常用指数列表
COMMON_INDICES = {
    "000300.XSHG": "沪深300",
    "399905.XSHE": "中证500",
    "399006.XSHE": "创业板指",
    "000016.XSHG": "上证50",
    "000852.XSHG": "中证1000",
    "000001.XSHG": "上证指数",
    "399001.XSHE": "深证成指",
}

# 默认股票池
DEFAULT_STOCKS = {
    "600519.XSHG": "贵州茅台",
    "000858.XSHE": "五粮液",
    "000333.XSHE": "美的集团",
    "600036.XSHG": "招商银行",
    "601318.XSHG": "中国平安",
    "000651.XSHE": "格力电器",
    "600000.XSHG": "浦发银行",
    "601166.XSHG": "兴业银行",
}


def preheat_etf_data(etfs=None, start_date=None, end_date=None):
    """预热ETF数据"""
    if etfs is None:
        etfs = COMMON_ETFS

    print(f"\n{'='*60}")
    print("预热ETF数据")
    print(f"{'='*60}")

    from jk2bt.market_data.etf import get_etf_daily

    success_count = 0
    for code, name in etfs.items():
        try:
            print(f"  下载 {code} ({name})...", end=" ")
            df = get_etf_daily(code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                print(f"✓ {len(df)} 条记录")
                success_count += 1
            else:
                print("✗ 无数据")
        except Exception as e:
            print(f"✗ 错误: {e}")

    print(f"\nETF数据预热完成: {success_count}/{len(etfs)} 成功")
    return success_count


def preheat_index_data(indices=None, start_date=None, end_date=None):
    """预热指数数据"""
    if indices is None:
        indices = COMMON_INDICES

    print(f"\n{'='*60}")
    print("预热指数数据")
    print(f"{'='*60}")

    from jk2bt.market_data.index import get_index_daily

    success_count = 0
    for code, name in indices.items():
        try:
            print(f"  下载 {code} ({name})...", end=" ")
            df = get_index_daily(code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                print(f"✓ {len(df)} 条记录")
                success_count += 1
            else:
                print("✗ 无数据")
        except Exception as e:
            print(f"✗ 错误: {e}")

    print(f"\n指数数据预热完成: {success_count}/{len(indices)} 成功")
    return success_count


def preheat_stock_data(stocks=None, start_date=None, end_date=None):
    """预热股票数据"""
    if stocks is None:
        stocks = DEFAULT_STOCKS

    print(f"\n{'='*60}")
    print("预热股票数据")
    print(f"{'='*60}")

    from jk2bt.market_data.stock import get_stock_daily

    success_count = 0
    for code, name in stocks.items():
        try:
            print(f"  下载 {code} ({name})...", end=" ")
            df = get_stock_daily(code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                print(f"✓ {len(df)} 条记录")
                success_count += 1
            else:
                print("✗ 无数据")
        except Exception as e:
            print(f"✗ 错误: {e}")

    print(f"\n股票数据预热完成: {success_count}/{len(stocks)} 成功")
    return success_count


def main():
    parser = argparse.ArgumentParser(description="数据预热脚本")
    parser.add_argument("--start", default=None, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", default=None, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=365, help="数据天数 (默认365天)")
    parser.add_argument("--etfs-only", action="store_true", help="只预热ETF数据")
    parser.add_argument("--indices-only", action="store_true", help="只预热指数数据")
    parser.add_argument("--stocks-only", action="store_true", help="只预热股票数据")

    args = parser.parse_args()

    # 设置日期范围
    if args.end:
        end_date = args.end
    else:
        end_date = datetime.now().strftime("%Y-%m-%d")

    if args.start:
        start_date = args.start
    else:
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    print(f"\n数据预热脚本")
    print(f"日期范围: {start_date} ~ {end_date}")

    total_success = 0
    total_count = 0

    if args.etfs_only:
        success = preheat_etf_data(start_date=start_date, end_date=end_date)
        total_success += success
        total_count += len(COMMON_ETFS)
    elif args.indices_only:
        success = preheat_index_data(start_date=start_date, end_date=end_date)
        total_success += success
        total_count += len(COMMON_INDICES)
    elif args.stocks_only:
        success = preheat_stock_data(start_date=start_date, end_date=end_date)
        total_success += success
        total_count += len(DEFAULT_STOCKS)
    else:
        # 预热所有数据
        total_success += preheat_etf_data(start_date=start_date, end_date=end_date)
        total_count += len(COMMON_ETFS)
        total_success += preheat_index_data(start_date=start_date, end_date=end_date)
        total_count += len(COMMON_INDICES)
        total_success += preheat_stock_data(start_date=start_date, end_date=end_date)
        total_count += len(DEFAULT_STOCKS)

    print(f"\n{'='*60}")
    print(f"数据预热完成: {total_success}/{total_count} 成功")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()