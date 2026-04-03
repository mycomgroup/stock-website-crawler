#!/usr/bin/env python3
"""
统一数据获取工具
支持港股、A股、美股财务数据获取

使用方法:
    python3 data_fetcher.py --market HK --code 09992 --year 2024
    python3 data_fetcher.py --market US --code MAT
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    import akshare as ak
    import pandas as pd
    import requests

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ 警告: AkShare未安装，港股数据获取将受限")
    print("安装命令: pip install akshare")


class DataFetcher:
    """统一数据获取类"""

    def __init__(self):
        self.load_api_keys()

    def load_api_keys(self):
        """加载API密钥"""
        # 从.env文件加载
        env_path = Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

        self.finnhub_key = os.getenv("FINNHUB_API_KEY", "")
        self.lixinger_token = os.getenv("LIXINGER_TOKEN", "")

    def get_hk_financial_data(self, stock_code, year=2024):
        """
        获取港股完整财务数据

        Args:
            stock_code: 股票代码，如 '09992'
            year: 年份，如 2024

        Returns:
            dict: 财务数据字典
        """
        if not AKSHARE_AVAILABLE:
            return {"error": "AkShare未安装"}

        year_str = f"{year}-12-31 00:00:00"

        try:
            print(f"📊 正在获取 {stock_code} {year}年财务数据...")

            # 获取现金流量表
            cf = ak.stock_financial_hk_report_em(stock=stock_code, symbol="现金流量表")
            ocf = cf[
                (cf["REPORT_DATE"] == year_str)
                & (cf["STD_ITEM_NAME"] == "经营业务现金净额")
            ]["AMOUNT"]

            # 资本开支
            capex_fix = cf[
                (cf["REPORT_DATE"] == year_str)
                & (cf["STD_ITEM_NAME"] == "购建固定资产")
            ]["AMOUNT"]
            capex_intangible = cf[
                (cf["REPORT_DATE"] == year_str)
                & (cf["STD_ITEM_NAME"] == "购建无形资产及其他资产")
            ]["AMOUNT"]

            # 获取资产负债表
            bs = ak.stock_financial_hk_report_em(stock=stock_code, symbol="资产负债表")
            cash = bs[
                (bs["REPORT_DATE"] == year_str)
                & (bs["STD_ITEM_NAME"] == "现金及等价物")
            ]["AMOUNT"]
            inventory = bs[
                (bs["REPORT_DATE"] == year_str) & (bs["STD_ITEM_NAME"] == "存货")
            ]["AMOUNT"]
            total_assets = bs[
                (bs["REPORT_DATE"] == year_str) & (bs["STD_ITEM_NAME"] == "总资产")
            ]["AMOUNT"]
            total_liabilities = bs[
                (bs["REPORT_DATE"] == year_str) & (bs["STD_ITEM_NAME"] == "总负债")
            ]["AMOUNT"]

            # 计算资本开支
            capex_val = 0
            if len(capex_fix) > 0:
                capex_val += float(capex_fix.values[0])
            if len(capex_intangible) > 0:
                capex_val += float(capex_intangible.values[0])

            result = {
                "stock_code": stock_code,
                "year": year,
                "operating_cash_flow": float(ocf.values[0]) if len(ocf) > 0 else None,
                "capex": capex_val,
                "cash": float(cash.values[0]) if len(cash) > 0 else None,
                "inventory": float(inventory.values[0]) if len(inventory) > 0 else None,
                "total_assets": float(total_assets.values[0])
                if len(total_assets) > 0
                else None,
                "total_liabilities": float(total_liabilities.values[0])
                if len(total_liabilities) > 0
                else None,
                "data_source": "AkShare",
                "status": "success",
            }

            print(
                f"✅ 成功获取 {len([v for v in result.values() if v is not None and not isinstance(v, str)])} 个字段"
            )
            return result

        except Exception as e:
            return {
                "stock_code": stock_code,
                "year": year,
                "error": str(e),
                "status": "failed",
            }

    def get_us_financial_data(self, symbol, year=None):
        """
        获取美股财务数据（使用Finnhub免费版）

        Args:
            symbol: 股票代码，如 'MAT'
            year: 年份（可选）

        Returns:
            dict: 财务数据字典
        """
        if not self.finnhub_key:
            return {"error": "FINNHUB_API_KEY未配置"}

        try:
            print(f"📊 正在获取 {symbol} 财务数据...")

            url = f"https://finnhub.io/api/v1/stock/financials-reported?symbol={symbol}&token={self.finnhub_key}&freq=annual"
            resp = requests.get(url, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                if "data" in data and len(data["data"]) > 0:
                    # 获取最新年份数据
                    latest = data["data"][0]
                    report_year = latest.get("year", "N/A")

                    result = {
                        "symbol": symbol,
                        "year": report_year,
                        "data_source": "Finnhub API (SEC)",
                        "status": "success",
                    }

                    # 解析利润表
                    if "report" in latest and "ic" in latest["report"]:
                        for item in latest["report"]["ic"]:
                            label = item.get("label", "").lower()
                            value = item.get("value")
                            if value and isinstance(value, (int, float)):
                                if "revenue" in label or "sales" in label:
                                    result["revenue"] = value / 1e9  # 转换为B
                                elif "gross profit" in label:
                                    result["gross_profit"] = value / 1e9
                                elif "net income" in label:
                                    result["net_income"] = value / 1e9

                    # 计算比率
                    if "revenue" in result and result["revenue"] > 0:
                        if "gross_profit" in result:
                            result["gross_margin"] = (
                                result["gross_profit"] / result["revenue"]
                            ) * 100
                        if "net_income" in result:
                            result["net_margin"] = (
                                result["net_income"] / result["revenue"]
                            ) * 100

                    print(f"✅ 成功获取 {symbol} {report_year}年数据")
                    return result
                else:
                    return {"symbol": symbol, "error": "无财务数据", "status": "failed"}
            else:
                return {
                    "symbol": symbol,
                    "error": f"API错误: {resp.status_code}",
                    "status": "failed",
                }

        except Exception as e:
            return {"symbol": symbol, "error": str(e), "status": "failed"}

    def get_stock_price(self, code, market="HK"):
        """
        获取股价数据

        Args:
            code: 股票代码
            market: 市场类型 (HK/US)

        Returns:
            DataFrame: 历史股价数据
        """
        if not AKSHARE_AVAILABLE:
            return None

        try:
            if market == "HK":
                df = ak.stock_hk_hist(
                    symbol=code,
                    period="daily",
                    start_date="20250101",
                    end_date="20260326",
                    adjust="qfq",
                )
                return df
            else:
                return None
        except Exception as e:
            print(f"❌ 获取股价失败: {e}")
            return None

    def compare_companies(self, companies):
        """
        对比多个公司的财务数据

        Args:
            companies: list of dict, 如 [{'code': '09992', 'market': 'HK', 'name': '泡泡玛特'}]

        Returns:
            DataFrame: 对比结果
        """
        results = []

        for comp in companies:
            market = comp.get("market", "HK")
            code = comp["code"]
            name = comp.get("name", code)

            print(f"\n🔍 正在获取 {name} ({code})...")

            if market == "HK":
                data = self.get_hk_financial_data(code, year=2024)
            else:
                data = self.get_us_financial_data(code)

            if data.get("status") == "success":
                data["name"] = name
                data["market"] = market
                results.append(data)

        if results:
            df = pd.DataFrame(results)
            return df
        else:
            return None


def main():
    parser = argparse.ArgumentParser(description="统一数据获取工具")
    parser.add_argument(
        "--market", choices=["HK", "US"], required=True, help="市场类型"
    )
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--year", type=int, default=2024, help="年份（港股）")
    parser.add_argument("--compare", action="store_true", help="对比模式")

    args = parser.parse_args()

    fetcher = DataFetcher()

    if args.compare:
        # 对比模式 - 硬编码示例
        companies = [
            {"code": "09992", "market": "HK", "name": "泡泡玛特"},
            {"code": "MAT", "market": "US", "name": "美泰"},
            {"code": "HAS", "market": "US", "name": "孩之宝"},
        ]
        df = fetcher.compare_companies(companies)
        if df is not None:
            print("\n📊 对比结果:")
            print(
                df[
                    ["name", "market", "revenue", "gross_margin", "net_margin"]
                ].to_string(index=False)
            )
    else:
        # 单只股票模式
        if args.market == "HK":
            result = fetcher.get_hk_financial_data(args.code, args.year)
        else:
            result = fetcher.get_us_financial_data(args.code)

        print("\n📋 结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
