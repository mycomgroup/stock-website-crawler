"""
通用策略验证示例 - 使用 StrategyRegimeAnalyzer 框架类

使用方法:
    1. 将此文件复制到聚宽 Research
    2. 确保 strategy_analyzer 目录在同一目录下
    3. 运行代码
"""

# ============================================================
# 导入框架
# ============================================================

# 如果在聚宽环境中，需要先上传框架文件
# 这里直接内联核心代码用于演示

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# 配置类
# ============================================================


class AnalyzerConfig:
    """分析器配置"""

    def __init__(self, **kwargs):
        self.start = kwargs.get("start", "2020-01-01")
        self.end = kwargs.get("end", "2026-03-28")
        self.freq = kwargs.get("freq", "quarterly")
        self.cost = kwargs.get("cost", 0.003)
        self.benchmarks = kwargs.get("benchmarks", ["399101.XSHE"])
        self.benchmark_names = kwargs.get(
            "benchmark_names",
            {
                "399101.XSHE": "中证2000",
                "000300.XSHG": "沪深300",
            },
        )
        self.recent_since = kwargs.get("recent_since", "2024-01-01")
        self.risk_free_rate = kwargs.get("risk_free_rate", 0.02)
        self.regime_thresholds = kwargs.get(
            "regime_thresholds",
            {
                "bull": 0.05,
                "mild_down": -0.05,
            },
        )
        self.parallel = kwargs.get("parallel", True)
        self.max_workers = kwargs.get("max_workers", 4)

    def get_benchmark_name(self, code):
        return self.benchmark_names.get(code, code)


# ============================================================
# 核心分析器
# ============================================================


class StrategyRegimeAnalyzer:
    """通用策略分行情验证框架"""

    def __init__(self, config):
        self.config = config
        self.strategies = {}
        self.strategy_names = []
        self.strategy_results = {}
        self.benchmark_results = {}
        self.merged_data = None
        self.total_periods = 0

    def register(self, name, select_fn, hold_n=10):
        """注册策略"""
        self.strategies[name] = {"select_fn": select_fn, "hold_n": hold_n}
        if name not in self.strategy_names:
            self.strategy_names.append(name)

    def _get_period_dates(self):
        """获取调仓日期"""
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

    def _filter_basic(self, stocks, date):
        """基础过滤"""
        try:
            is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
            stocks = is_st[is_st == False].index.tolist()
        except:
            pass
        return stocks

    def _run_single(self, select_fn, hold_n):
        """执行单个策略回测"""
        dates = self._get_period_dates()
        results = []
        prev_stocks = []

        for i, d in enumerate(dates[:-1]):
            d_str = str(d)
            next_d_str = str(dates[i + 1])

            try:
                selected = select_fn(d_str, hold_n)

                if not selected or len(selected) == 0:
                    results.append({"date": d, "ret": 0, "turnover": 0})
                    continue

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

                gross = ((p1 / p0) - 1).dropna().mean()
                turnover = len(set(selected) - set(prev_stocks)) / max(len(selected), 1)
                net_ret = gross - turnover * self.config.cost * 2

                results.append({"date": d, "ret": net_ret, "turnover": turnover})
                prev_stocks = selected

            except Exception as e:
                results.append({"date": d, "ret": 0, "turnover": 0})

        df = pd.DataFrame(results)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def _run_benchmark(self, index_code):
        """获取基准收益"""
        dates = self._get_period_dates()
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

    def run(self):
        """执行所有策略回测"""
        print("=" * 60)
        print("执行策略回测...")
        print("=" * 60)

        # 执行策略回测
        for name, params in self.strategies.items():
            print(f"  {name}...")
            self.strategy_results[name] = self._run_single(
                params["select_fn"], params["hold_n"]
            )

        # 获取基准数据
        print("\n获取基准数据...")
        for code in self.config.benchmarks:
            bench_name = self.config.get_benchmark_name(code)
            print(f"  {bench_name}...")
            self.benchmark_results[bench_name] = self._run_benchmark(code)

        # 合并数据
        self._merge_data()

        print(f"\n回测完成! 共{self.total_periods}个周期")

    def _merge_data(self):
        """合并数据"""
        first_strategy = list(self.strategy_results.keys())[0]
        merged = self.strategy_results[first_strategy][["date"]].copy()

        for name, df in self.strategy_results.items():
            merged = merged.merge(
                df[["date", "ret"]].rename(columns={"ret": name}), on="date", how="left"
            )

        for name, df in self.benchmark_results.items():
            merged = merged.merge(
                df[["date", "ret"]].rename(columns={"ret": name}), on="date", how="left"
            )

        self.merged_data = merged
        self.total_periods = len(merged)

    def _calc_risk(self, returns):
        """计算风险指标"""
        if len(returns) < 2:
            return {}

        periods_per_year = 12 if self.config.freq == "monthly" else 4

        cum_ret = (1 + returns).prod() - 1
        years = len(returns) / periods_per_year
        ann_ret = (1 + cum_ret) ** (1 / years) - 1 if years > 0 else 0
        ann_vol = returns.std() * np.sqrt(periods_per_year)
        sharpe = (ann_ret - self.config.risk_free_rate) / ann_vol if ann_vol > 0 else 0

        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.cummax()
        drawdown = (cum_returns - running_max) / running_max
        max_dd = abs(drawdown.min())

        calmar = ann_ret / max_dd if max_dd > 0 else 0
        win_rate = (returns > 0).sum() / len(returns)

        return {
            "cum_ret": cum_ret,
            "ann_ret": ann_ret,
            "ann_vol": ann_vol,
            "sharpe": sharpe,
            "max_dd": max_dd,
            "calmar": calmar,
            "win_rate": win_rate,
        }

    def _classify_regime(self, ret):
        """市场状态分类"""
        thresholds = self.config.regime_thresholds
        if pd.isna(ret):
            return "未知"
        if ret > thresholds["bull"]:
            return f"牛市(涨>{thresholds['bull']:.0%})"
        elif ret > 0:
            return f"温和上涨(0~{thresholds['bull']:.0%})"
        elif ret > thresholds["mild_down"]:
            return f"温和下跌({thresholds['mild_down']:.0%}~0)"
        else:
            return f"熊市(跌<{thresholds['mild_down']:.0%})"

    def analyze(self):
        """执行全部分析"""
        if self.merged_data is None:
            raise ValueError("请先执行 run()")

        print("\n" + "=" * 60)
        print("执行分析...")
        print("=" * 60)

        # 获取主基准
        main_benchmark = list(self.benchmark_results.keys())[0]

        # 年度分析
        print("\n1. 年度收益分析...")
        self.merged_data["year"] = self.merged_data["date"].dt.year
        all_cols = self.strategy_names + list(self.benchmark_results.keys())
        self.yearly_results = (
            self.merged_data.groupby("year")
            .agg(
                {
                    col: lambda x: (1 + x.dropna()).prod() - 1
                    if len(x.dropna()) > 0
                    else 0
                    for col in all_cols
                }
            )
            .round(4)
        )

        # 风险分析
        print("2. 风险指标分析...")
        self.risk_results = {}
        for name in all_cols:
            self.risk_results[name] = self._calc_risk(self.merged_data[name])

        # 市场状态分析
        print("3. 市场状态分析...")
        self.merged_data["regime"] = self.merged_data[main_benchmark].apply(
            self._classify_regime
        )

        # 择时分析
        print("4. 择时效果分析...")
        self.merged_data["benchmark_lag1"] = self.merged_data[main_benchmark].shift(1)

        # 近期分析
        print("5. 近期表现分析...")
        self.recent_results = {}
        recent = self.merged_data[self.merged_data["date"] >= self.config.recent_since]
        for name in all_cols:
            self.recent_results[name] = {
                "cum_ret": (1 + recent[name]).prod() - 1,
                "mean_ret": recent[name].mean(),
            }

        print("\n分析完成!")

    def report(self, output_path=None):
        """生成报告"""
        # 构建 Markdown 报告
        lines = []
        lines.append("# 策略分行情验证报告\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**验证区间**: {self.config.start} ~ {self.config.end}")
        lines.append(
            f"**调仓频率**: {'月度' if self.config.freq == 'monthly' else '季度'}"
        )
        lines.append(f"**交易成本**: {self.config.cost:.2%}/次\n")
        lines.append("---\n")

        # 年度收益
        lines.append("## 一、按年度收益统计\n")
        lines.append(self.yearly_results.to_markdown())
        lines.append("\n---\n")

        # 风险指标
        lines.append("## 二、风险指标\n")
        risk_df = pd.DataFrame(self.risk_results).T
        risk_df = risk_df.round(4)
        lines.append(risk_df.to_markdown())
        lines.append("\n---\n")

        # 近期表现
        lines.append("## 三、近期表现\n")
        recent_df = pd.DataFrame(self.recent_results).T
        recent_df = recent_df.round(4)
        lines.append(recent_df.to_markdown())
        lines.append("\n---\n")

        content = "\n".join(lines)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"报告已生成: {output_path}")

        return content

    def print_summary(self):
        """打印摘要"""
        print("\n" + "=" * 60)
        print("策略验证摘要")
        print("=" * 60)

        print("\n【年度收益】")
        print(self.yearly_results.to_string())

        print("\n【风险指标】")
        for name in self.strategy_names:
            if name in self.risk_results:
                risk = self.risk_results[name]
                print(f"\n{name}:")
                print(f"  年化收益: {risk.get('ann_ret', 0):.1%}")
                print(f"  夏普比率: {risk.get('sharpe', 0):.2f}")
                print(f"  最大回撤: {risk.get('max_dd', 0):.1%}")

        print(f"\n【近期表现 ({self.config.recent_since}至今)】")
        for name in self.strategy_names:
            if name in self.recent_results:
                info = self.recent_results[name]
                print(f"  {name}: 累计{info.get('cum_ret', 0):.1%}")


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    # 定义策略
    def select_guojiu(date, n=10):
        """国九条筛选型"""
        q = (
            query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                indicator.inc_net_profit_year_on_year,
            )
            .filter(
                valuation.market_cap > 10,
                valuation.market_cap < 50,
                valuation.pe_ratio > 0,
                valuation.pe_ratio < 40,
                indicator.inc_net_profit_year_on_year > 0,
            )
            .order_by(valuation.pe_ratio.asc())
            .limit(n * 3)
        )

        df = get_fundamentals(q, date=date)
        stks = [
            c
            for c in df["code"].tolist()
            if not get_extras("is_st", [c], end_date=date, count=1).iloc[-1][0]
        ]
        return stks[:n]

    def select_micro_cap(date, n=10):
        """微盘再平衡型"""
        q = (
            query(valuation.code, valuation.market_cap, valuation.pb_ratio)
            .filter(
                valuation.market_cap > 5,
                valuation.market_cap < 30,
                valuation.pb_ratio > 0,
                valuation.pb_ratio < 3,
            )
            .order_by(valuation.market_cap.asc())
            .limit(n * 3)
        )

        df = get_fundamentals(q, date=date)
        stks = [
            c
            for c in df["code"].tolist()
            if not get_extras("is_st", [c], end_date=date, count=1).iloc[-1][0]
        ]
        return stks[:n]

    # 配置
    config = AnalyzerConfig(
        start="2020-01-01",
        end="2026-03-28",
        freq="quarterly",
        cost=0.003,
        benchmarks=["399101.XSHE", "000300.XSHG"],
    )

    # 创建分析器
    analyzer = StrategyRegimeAnalyzer(config)
    analyzer.register("国九条筛选型", select_guojiu, hold_n=10)
    analyzer.register("微盘再平衡型", select_micro_cap, hold_n=10)

    # 运行
    analyzer.run()
    analyzer.analyze()
    analyzer.print_summary()

    # 生成报告
    analyzer.report(output_path="strategy_report.md")
