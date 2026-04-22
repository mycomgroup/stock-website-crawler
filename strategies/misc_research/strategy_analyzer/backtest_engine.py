"""
回测引擎模块
"""

import pandas as pd
import numpy as np
from typing import List, Callable, Dict, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class BacktestEngine:
    """回测引擎"""

    def __init__(self, config):
        """
        Args:
            config: AnalyzerConfig 配置对象
        """
        self.config = config
        self._jqdata_available = False
        self._check_jqdata()

    def _check_jqdata(self):
        """检查 jqdata 是否可用"""
        try:
            from jqdata import get_trade_days

            self._jqdata_available = True
        except ImportError:
            self._jqdata_available = False

    def get_period_dates(self) -> List:
        """获取调仓日期列表

        Returns:
            调仓日期列表
        """
        if not self._jqdata_available:
            raise ImportError("jqdata not available")

        from jqdata import get_trade_days

        days = get_trade_days(self.config.start, self.config.end)
        result, last_period = [], None

        for d in days:
            if self.config.freq == "monthly":
                period = d.month
            elif self.config.freq == "quarterly":
                period = (d.month - 1) // 3
            else:
                raise ValueError(f"Unsupported freq: {self.config.freq}")

            if period != last_period:
                result.append(d)
                last_period = period

        return result

    def filter_basic(self, stocks: List[str], date: str) -> List[str]:
        """基础过滤 (ST等)

        Args:
            stocks: 股票列表
            date: 日期

        Returns:
            过滤后的股票列表
        """
        if not self._jqdata_available:
            return stocks

        try:
            from jqdata import get_extras

            is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
            stocks = is_st[is_st == False].index.tolist()
        except:
            pass
        return stocks

    def run_single(self, select_fn: Callable, hold_n: int = 10) -> pd.DataFrame:
        """执行单个策略回测

        Args:
            select_fn: 选股函数 (date: str, n: int) -> List[str]
            hold_n: 持仓数量

        Returns:
            包含 date, ret, turnover 的 DataFrame
        """
        if not self._jqdata_available:
            raise ImportError("jqdata not available")

        from jqdata import get_price

        dates = self.get_period_dates()
        results = []
        prev_stocks = []

        for i, d in enumerate(dates[:-1]):
            d_str = str(d)
            next_d_str = str(dates[i + 1])

            try:
                selected = select_fn(d_str, hold_n)

                if not selected or len(selected) == 0:
                    results.append({"date": d, "ret": 0, "turnover": 0, "n": 0})
                    continue

                # 获取价格
                p0 = get_price(
                    selected, end_date=d_str, count=1, fields=["close"], panel=False
                )
                p1 = get_price(
                    selected,
                    end_date=next_d_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                )

                p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
                p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]

                # 计算收益
                gross = ((p1 / p0) - 1).dropna().mean()
                turnover = len(set(selected) - set(prev_stocks)) / max(len(selected), 1)
                net_ret = gross - turnover * self.config.cost * 2

                results.append(
                    {
                        "date": d,
                        "ret": net_ret,
                        "turnover": turnover,
                        "n": len(selected),
                    }
                )
                prev_stocks = selected

            except Exception as e:
                results.append({"date": d, "ret": 0, "turnover": 0, "n": 0})

        df = pd.DataFrame(results)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def run_benchmark(self, index_code: str) -> pd.DataFrame:
        """获取基准指数收益

        Args:
            index_code: 指数代码

        Returns:
            包含 date, ret 的 DataFrame
        """
        if not self._jqdata_available:
            raise ImportError("jqdata not available")

        from jqdata import get_price

        dates = self.get_period_dates()
        results = []

        for i, d in enumerate(dates[:-1]):
            d_str = str(d)
            next_d_str = str(dates[i + 1])

            try:
                p0 = get_price(
                    index_code, end_date=d_str, count=1, fields=["close"], panel=False
                )["close"].iloc[-1]
                p1 = get_price(
                    index_code,
                    end_date=next_d_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                )["close"].iloc[-1]
                ret = (p1 / p0) - 1
                results.append({"date": d, "ret": ret})
            except:
                results.append({"date": d, "ret": 0})

        df = pd.DataFrame(results)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def run_all(self, strategies: Dict[str, Dict]) -> Dict[str, pd.DataFrame]:
        """并行执行所有策略回测

        Args:
            strategies: {name: {"select_fn": fn, "hold_n": n}}

        Returns:
            {name: DataFrame}
        """
        results = {}

        if self.config.parallel and len(strategies) > 1:
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                futures = {}
                for name, params in strategies.items():
                    future = executor.submit(
                        self.run_single, params["select_fn"], params.get("hold_n", 10)
                    )
                    futures[future] = name

                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        results[name] = future.result()
                    except Exception as e:
                        print(f"Strategy {name} failed: {e}")
        else:
            for name, params in strategies.items():
                try:
                    results[name] = self.run_single(
                        params["select_fn"], params.get("hold_n", 10)
                    )
                except Exception as e:
                    print(f"Strategy {name} failed: {e}")

        return results

    def run_benchmarks(self, index_codes: List[str]) -> Dict[str, pd.DataFrame]:
        """获取所有基准数据

        Args:
            index_codes: 指数代码列表

        Returns:
            {code: DataFrame}
        """
        results = {}
        for code in index_codes:
            try:
                results[code] = self.run_benchmark(code)
            except Exception as e:
                print(f"Benchmark {code} failed: {e}")
        return results
