"""
validation/data_collector.py
数据采集器 - 本地数据源和 JoinQuant 数据源
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging
import json
import os

logger = logging.getLogger(__name__)


class LocalDataSource:
    """本地数据源 (AkShare)"""

    def __init__(self):
        self._ak = None

    @property
    def ak(self):
        """延迟导入 AkShare"""
        if self._ak is None:
            import akshare as ak
            self._ak = ak
        return self._ak

    def _normalize_code(self, code: str) -> str:
        """将聚宽代码转换为 AkShare 代码"""
        if ".XSHG" in code:
            return code.replace(".XSHG", "")
        elif ".XSHE" in code:
            return code.replace(".XSHE", "")
        return code

    def _get_prefix(self, code: str) -> str:
        """获取股票代码前缀 (sh/sz)"""
        pure_code = self._normalize_code(code)
        if pure_code.startswith("6"):
            return "sh"
        return "sz"

    def get_valuation_data(self, stocks: List[str], date: str) -> pd.DataFrame:
        """
        获取估值数据 (PE/PB/市值等)

        Args:
            stocks: 股票代码列表
            date: 日期 (YYYY-MM-DD)

        Returns:
            DataFrame with columns: code, date, pe, pb, market_cap, circulating_market_cap
        """
        results = []
        target_date = pd.to_datetime(date)

        for stock in stocks:
            try:
                pure_code = self._normalize_code(stock)
                df = self.ak.stock_a_lg_indicator(symbol=pure_code)

                if df is not None and not df.empty:
                    # 标准化列名
                    col_map = {
                        "日期": "date",
                        "pe": "pe",
                        "pe_ttm": "pe_ttm",
                        "pb": "pb",
                        "ps": "ps",
                        "dv_ratio": "dividend_ratio",
                        "total_mv": "market_cap",
                        "circ_mv": "circulating_market_cap",
                    }
                    df = df.rename(columns=col_map)

                    if "date" in df.columns:
                        df["date"] = pd.to_datetime(df["date"])
                        row = df[df["date"] == target_date]
                        if row.empty:
                            # 取最近的日期
                            row = df[df["date"] <= target_date].tail(1)

                        if not row.empty:
                            results.append({
                                "code": stock,
                                "date": date,
                                "pe": row["pe"].values[0] if "pe" in row else None,
                                "pe_ttm": row["pe_ttm"].values[0] if "pe_ttm" in row else None,
                                "pb": row["pb"].values[0] if "pb" in row else None,
                                "ps": row["ps"].values[0] if "ps" in row else None,
                                "market_cap": row["market_cap"].values[0] if "market_cap" in row else None,
                                "circulating_market_cap": row["circulating_market_cap"].values[0] if "circulating_market_cap" in row else None,
                            })
            except Exception as e:
                logger.warning(f"获取 {stock} 估值数据失败: {e}")

        return pd.DataFrame(results)

    def get_trade_status(self, stocks: List[str], date: str) -> pd.DataFrame:
        """
        获取交易状态数据 (涨跌停/ST/停牌)

        Args:
            stocks: 股票代码列表
            date: 日期 (YYYY-MM-DD)

        Returns:
            DataFrame with columns: code, date, high_limit, low_limit, is_st, paused
        """
        results = []

        # 获取 ST 列表
        st_stocks = set()
        try:
            st_df = self.ak.stock_zh_a_st_em()
            if st_df is not None and not st_df.empty:
                st_stocks = set(st_df["代码"].tolist())
        except Exception as e:
            logger.warning(f"获取 ST 列表失败: {e}")

        # 获取停牌列表
        paused_stocks = set()
        try:
            stop_df = self.ak.stock_zh_a_stop_em()
            if stop_df is not None and not stop_df.empty:
                paused_stocks = set(stop_df["代码"].tolist())
        except Exception as e:
            logger.warning(f"获取停牌列表失败: {e}")

        for stock in stocks:
            try:
                pure_code = self._normalize_code(stock)

                # 获取前收盘价计算涨跌停价
                prefix = self._get_prefix(stock)
                ak_code = f"{prefix}{pure_code}"

                try:
                    df = self.ak.stock_zh_a_hist(
                        symbol=pure_code,
                        period="daily",
                        start_date=(pd.to_datetime(date) - timedelta(days=5)).strftime("%Y%m%d"),
                        end_date=pd.to_datetime(date).strftime("%Y%m%d"),
                        adjust="",
                    )
                except Exception:
                    # 尝试东方财富
                    df = self.ak.stock_zh_a_hist_min_em(symbol=ak_code, period="daily", adjust="")

                high_limit = None
                low_limit = None
                prev_close = None

                if df is not None and not df.empty:
                    # 标准化列名
                    if "收盘" in df.columns:
                        df = df.rename(columns={"收盘": "close", "日期": "date"})
                    if "date" not in df.columns and df.index.name == "date":
                        df = df.reset_index()

                    if "date" in df.columns:
                        df["date"] = pd.to_datetime(df["date"])
                        target_date = pd.to_datetime(date)
                        row = df[df["date"] <= target_date].tail(2)

                        if len(row) >= 2:
                            prev_close = row.iloc[-2]["close"]
                            curr_close = row.iloc[-1]["close"]
                        elif len(row) == 1:
                            prev_close = row.iloc[0]["close"]

                # 计算涨跌停价
                if prev_close is not None and prev_close > 0:
                    limit_ratio = 0.10  # 主板 10%
                    if pure_code.startswith("300") or pure_code.startswith("688"):
                        limit_ratio = 0.20  # 创业板/科创板 20%
                    if pure_code in st_stocks:
                        limit_ratio = 0.05  # ST 5%

                    high_limit = round(prev_close * (1 + limit_ratio), 2)
                    low_limit = round(prev_close * (1 - limit_ratio), 2)

                results.append({
                    "code": stock,
                    "date": date,
                    "high_limit": high_limit,
                    "low_limit": low_limit,
                    "is_st": pure_code in st_stocks,
                    "paused": pure_code in paused_stocks,
                    "prev_close": prev_close,
                })

            except Exception as e:
                logger.warning(f"获取 {stock} 交易状态失败: {e}")
                results.append({
                    "code": stock,
                    "date": date,
                    "high_limit": None,
                    "low_limit": None,
                    "is_st": None,
                    "paused": None,
                    "prev_close": None,
                })

        return pd.DataFrame(results)

    def get_factor_data(self, stocks: List[str], date: str, factors: List[str]) -> pd.DataFrame:
        """
        获取因子数据 (手动计算)

        Args:
            stocks: 股票代码列表
            date: 日期
            factors: 因子列表

        Returns:
            DataFrame with factor values
        """
        results = []

        for stock in stocks:
            try:
                pure_code = self._normalize_code(stock)
                factor_values = {"code": stock, "date": date}

                # 获取历史数据计算因子
                df = self.ak.stock_zh_a_hist(
                    symbol=pure_code,
                    period="daily",
                    start_date=(pd.to_datetime(date) - timedelta(days=60)).strftime("%Y%m%d"),
                    end_date=pd.to_datetime(date).strftime("%Y%m%d"),
                    adjust="qfq",
                )

                if df is not None and not df.empty:
                    closes = df["收盘"].values if "收盘" in df.columns else df["close"].values

                    # 计算动量因子
                    if "momentum_20" in factors and len(closes) >= 20:
                        factor_values["momentum_20"] = (closes[-1] / closes[-20] - 1) * 100

                    # 计算波动率因子
                    if "volatility_20" in factors and len(closes) >= 20:
                        returns = np.diff(closes[-21:]) / closes[-21:-1]
                        factor_values["volatility_20"] = np.std(returns) * np.sqrt(252) * 100

                    # 计算均线因子
                    if "ma_5" in factors and len(closes) >= 5:
                        factor_values["ma_5"] = np.mean(closes[-5:])
                    if "ma_20" in factors and len(closes) >= 20:
                        factor_values["ma_20"] = np.mean(closes[-20:])

                results.append(factor_values)

            except Exception as e:
                logger.warning(f"获取 {stock} 因子数据失败: {e}")
                results.append({"code": stock, "date": date})

        return pd.DataFrame(results)


class JQNotebookSource:
    """JoinQuant Notebook 数据源"""

    def __init__(self, notebook_runner_path: str = None):
        """
        Args:
            notebook_runner_path: joinquant_notebook skill 路径
        """
        self.notebook_runner_path = notebook_runner_path or "lib/stock-website-crawler/skills/joinquant_notebook"

    def _generate_collector_code(self, stocks: List[str], date: str, data_type: str) -> str:
        """生成在 JQ Notebook 中执行的数据采集代码"""
        stocks_str = json.dumps(stocks)

        if data_type == "valuation":
            code = f'''
import json
from jqdata import *

stocks = {stocks_str}
date = "{date}"

results = []
for stock in stocks:
    try:
        q = query(valuation).filter(valuation.code == stock)
        df = get_fundamentals(q, date)
        if df is not None and not df.empty:
            row = df.iloc[0]
            results.append({{
                "code": stock,
                "date": date,
                "pe": float(row.get("pe_ratio", 0)) if row.get("pe_ratio") else None,
                "pb": float(row.get("pb_ratio", 0)) if row.get("pb_ratio") else None,
                "market_cap": float(row.get("market_cap", 0)) if row.get("market_cap") else None,
                "circulating_market_cap": float(row.get("circulating_market_cap", 0)) if row.get("circulating_market_cap") else None,
            }})
    except Exception as e:
        print(f"Error {{stock}}: {{e}}")

print("=== RESULT ===")
print(json.dumps(results, ensure_ascii=False))
'''
            return code

        elif data_type == "trade_status":
            code = f'''
import json
from jqdata import *

stocks = {stocks_str}
date = "{date}"

results = []
current_data = get_current_data(stocks)

for stock in stocks:
    try:
        data = current_data[stock]
        results.append({{
            "code": stock,
            "date": date,
            "high_limit": float(data.high_limit) if data.high_limit else None,
            "low_limit": float(data.low_limit) if data.low_limit else None,
            "is_st": bool(data.is_st),
            "paused": bool(data.paused),
        }})
    except Exception as e:
        print(f"Error {{stock}}: {{e}}")

print("=== RESULT ===")
print(json.dumps(results, ensure_ascii=False))
'''
            return code

        elif data_type == "factors":
            code = f'''
import json
from jqdata import *

stocks = {stocks_str}
date = "{date}"

results = []
for stock in stocks:
    try:
        # 获取因子值
        factors = get_factor_values([stock], ["momentum_20", "volatility_20"], date, date)
        if factors is not None and not factors.empty:
            row = factors.iloc[0]
            results.append({{
                "code": stock,
                "date": date,
                "momentum_20": float(row.get("momentum_20", 0)) if "momentum_20" in row else None,
                "volatility_20": float(row.get("volatility_20", 0)) if "volatility_20" in row else None,
            }})
    except Exception as e:
        print(f"Error {{stock}}: {{e}}")

print("=== RESULT ===")
print(json.dumps(results, ensure_ascii=False))
'''
            return code

        return ""

    def collect_data(self, stocks: List[str], date: str, data_type: str,
                     output_file: str = None) -> pd.DataFrame:
        """
        通过 JoinQuant Notebook 采集数据

        注意: 需要手动运行生成的代码，或使用 joinquant_notebook skill 自动执行
        """
        code = self._generate_collector_code(stocks, date, data_type)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(code)

        logger.info(f"生成的采集代码已保存到: {output_file}")
        logger.info("请使用 joinquant_notebook skill 执行此代码")

        return pd.DataFrame()  # 实际数据需要执行后获取

    def parse_result_file(self, result_file: str) -> pd.DataFrame:
        """解析 JQ Notebook 输出结果"""
        with open(result_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 查找结果标记
        if "=== RESULT ===" in content:
            result_str = content.split("=== RESULT ===")[1].strip()
            try:
                results = json.loads(result_str)
                return pd.DataFrame(results)
            except json.JSONDecodeError:
                logger.error("解析结果失败")

        return pd.DataFrame()


class DataCollector:
    """双源数据采集器"""

    def __init__(self, config=None):
        self.config = config or ValidationConfig()
        self.local_source = LocalDataSource()
        self.jq_source = JQNotebookSource()

    def collect_all(self, stocks: List[str], date: str, data_types: List[str]) -> Dict[str, Dict]:
        """
        采集所有指定类型的数据

        Returns:
            {
                "valuation": {"local": DataFrame, "jq": DataFrame},
                "trade_status": {"local": DataFrame, "jq": DataFrame},
                ...
            }
        """
        results = {}

        for data_type in data_types:
            local_df = pd.DataFrame()
            jq_df = pd.DataFrame()

            if data_type == "valuation":
                local_df = self.local_source.get_valuation_data(stocks, date)
                # JQ 数据需要单独执行
                jq_code_file = f"validation_results/jq_collector_{data_type}_{date}.py"
                self.jq_source.collect_data(stocks, date, data_type, jq_code_file)

            elif data_type == "trade_status":
                local_df = self.local_source.get_trade_status(stocks, date)
                jq_code_file = f"validation_results/jq_collector_{data_type}_{date}.py"
                self.jq_source.collect_data(stocks, date, data_type, jq_code_file)

            elif data_type == "factors":
                factors = ["momentum_20", "volatility_20"]
                local_df = self.local_source.get_factor_data(stocks, date, factors)
                jq_code_file = f"validation_results/jq_collector_{data_type}_{date}.py"
                self.jq_source.collect_data(stocks, date, data_type, jq_code_file)

            results[data_type] = {
                "local": local_df,
                "jq": jq_df,
            }

        return results

    def collect_batch(self, stocks: List[str], dates: List[str],
                      data_types: List[str], batch_size: int = 50) -> Dict:
        """批量采集数据"""
        results = {}

        for date in dates:
            logger.info(f"采集日期: {date}")
            date_results = self.collect_all(stocks, date, data_types)
            results[date] = date_results

        return results


# 导入 ValidationConfig
from .config import ValidationConfig