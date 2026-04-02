"""
红利小盘策略因子有效性分析代码示例
用于验证PE、PB、ROE、净利润增长、市值等因子在小市值区间的有效性
"""

from jqdatasdk import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

# 聚宽登录（需要替换为实际账号密码）
# auth('username', 'password')


class FactorAnalyzer:
    """因子有效性分析器"""

    def __init__(self, start_date="2020-01-01", end_date="2025-12-31"):
        self.start_date = start_date
        self.end_date = end_date
        self.trade_days = get_trade_days(start_date, end_date)

    def get_smallcap_universe(self, watch_date, min_cap=15, max_cap=60):
        """获取小市值股票池"""
        # 获取所有股票
        all_stocks = get_all_securities(types=["stock"], date=watch_date)

        # 过滤上市时间
        all_stocks = all_stocks[
            all_stocks["start_date"] <= watch_date - timedelta(days=180)
        ]
        stocks = all_stocks.index.tolist()

        # 过滤ST股票
        is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        # 过滤停牌股票
        paused = get_price(
            stocks, end_date=watch_date, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()

        # 过滤科创板
        stocks = [s for s in stocks if not s.startswith("688")]

        # 市值筛选
        q = query(valuation.code, valuation.market_cap).filter(
            valuation.code.in_(stocks),
            valuation.market_cap >= min_cap,
            valuation.market_cap <= max_cap,
        )

        df = get_fundamentals(q, date=watch_date)
        return df["code"].tolist()

    def get_factor_data(self, stocks, watch_date):
        """获取因子数据"""
        q = query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.inc_net_profit_to_shareholders_year_on_year,
            indicator.dividend_yield_ratio,
        ).filter(
            valuation.code.in_(stocks), valuation.pe_ratio > 0, valuation.pe_ratio < 100
        )

        df = get_fundamentals(q, date=watch_date)
        df = df.drop_duplicates("code")
        return df

    def get_forward_return(self, stocks, watch_date, hold_days=5):
        """获取未来N日收益率"""
        future_date = get_trade_days(
            watch_date, watch_date + timedelta(days=hold_days * 2), count=hold_days + 1
        )[-1]

        prices = get_price(
            stocks, end_date=future_date, count=1, fields=["close"], panel=False
        )

        prices_now = get_price(
            stocks, end_date=watch_date, count=1, fields=["close"], panel=False
        )

        # 计算收益率
        returns = (
            prices.pivot(index="time", columns="code", values="close").iloc[-1]
            / prices_now.pivot(index="time", columns="code", values="close").iloc[-1]
            - 1
        )

        return returns

    def calculate_ic(self, factor_values, forward_returns):
        """计算Rank IC"""
        # 去除NaN
        valid_data = pd.DataFrame(
            {"factor": factor_values, "return": forward_returns}
        ).dropna()

        if len(valid_data) < 30:
            return np.nan

        # 计算秩相关系数
        ic = valid_data["factor"].corr(valid_data["return"], method="spearman")
        return ic

    def calculate_quantile_returns(self, factor_values, forward_returns, n_quantiles=5):
        """计算分层收益"""
        data = pd.DataFrame(
            {"factor": factor_values, "return": forward_returns}
        ).dropna()

        if len(data) < n_quantiles * 10:
            return None

        # 分层
        data["quantile"] = (
            pd.qcut(data["factor"], n_quantiles, labels=False, duplicates="drop") + 1
        )

        # 计算各层平均收益
        quantile_returns = data.groupby("quantile")["return"].mean()
        return quantile_returns

    def analyze_factor(self, factor_name, ascending=True):
        """分析单个因子的IC和分层收益"""
        ic_series = []
        quantile_returns_all = []

        for date in self.trade_days[::5]:  # 每5个交易日分析一次
            try:
                # 获取股票池
                stocks = self.get_smallcap_universe(date)
                if len(stocks) < 50:
                    continue

                # 获取因子数据
                factor_data = self.get_factor_data(stocks, date)
                if len(factor_data) < 50:
                    continue

                # 获取未来收益
                forward_returns = self.get_forward_return(
                    factor_data["code"].tolist(), date
                )

                # 获取因子值
                factor_values = factor_data.set_index("code")[factor_name]

                # 计算IC
                ic = self.calculate_ic(factor_values, forward_returns)
                if not np.isnan(ic):
                    ic_series.append(ic)

                # 计算分层收益
                # 注意：对于PE、PB、市值，越低越好，需要取负
                if factor_name in ["pe_ratio", "pb_ratio", "market_cap"]:
                    factor_values = -factor_values

                quantile_returns = self.calculate_quantile_returns(
                    factor_values, forward_returns
                )
                if quantile_returns is not None:
                    quantile_returns_all.append(quantile_returns)

            except Exception as e:
                continue

        # 汇总结果
        results = {
            "factor": factor_name,
            "ic_mean": np.mean(ic_series) if ic_series else np.nan,
            "ic_std": np.std(ic_series) if ic_series else np.nan,
            "ir": np.mean(ic_series) / np.std(ic_series)
            if ic_series and np.std(ic_series) > 0
            else np.nan,
            "ic_positive_rate": np.mean([ic > 0 for ic in ic_series])
            if ic_series
            else np.nan,
            "observation_days": len(ic_series),
        }

        # 分层收益汇总
        if quantile_returns_all:
            quantile_df = pd.DataFrame(quantile_returns_all)
            results["quantile_returns"] = quantile_df.mean().to_dict()
            results["long_short_return"] = (
                quantile_df[5].mean() - quantile_df[1].mean()
                if 5 in quantile_df.columns
                else np.nan
            )

        return results

    def calculate_factor_correlation(self, watch_date):
        """计算因子相关性"""
        stocks = self.get_smallcap_universe(watch_date)
        factor_data = self.get_factor_data(stocks, watch_date)

        # 计算相关系数矩阵
        factors = [
            "pe_ratio",
            "pb_ratio",
            "roe",
            "inc_net_profit_to_shareholders_year_on_year",
            "market_cap",
        ]

        corr_matrix = factor_data[factors].corr()
        return corr_matrix


def run_factor_analysis():
    """运行完整的因子有效性分析"""
    print("=" * 60)
    print("红利小盘策略因子有效性分析")
    print("=" * 60)

    # 初始化分析器
    analyzer = FactorAnalyzer(start_date="2020-01-01", end_date="2025-12-31")

    # 待分析因子
    factors = {
        "pe_ratio": "PE因子（市盈率）",
        "pb_ratio": "PB因子（市净率）",
        "roe": "ROE因子（净资产收益率）",
        "inc_net_profit_to_shareholders_year_on_year": "净利润增长因子",
        "market_cap": "市值因子",
    }

    # 分析各因子
    results = []
    for factor_code, factor_name in factors.items():
        print(f"\n分析因子: {factor_name}")
        result = analyzer.analyze_factor(factor_code)
        result["factor_name"] = factor_name
        results.append(result)

    # 生成报告
    print("\n" + "=" * 60)
    print("因子IC/IR值分析结果")
    print("=" * 60)

    results_df = pd.DataFrame(results)
    print(
        results_df[
            [
                "factor_name",
                "ic_mean",
                "ic_std",
                "ir",
                "ic_positive_rate",
                "observation_days",
            ]
        ].to_string()
    )

    # 因子相关性分析
    print("\n" + "=" * 60)
    print("因子相关性矩阵")
    print("=" * 60)

    corr_matrix = analyzer.calculate_factor_correlation("2025-12-31")
    print(corr_matrix.round(2).to_string())

    # 输出建议
    print("\n" + "=" * 60)
    print("因子有效性判断")
    print("=" * 60)

    for _, row in results_df.iterrows():
        ic_mean = row["ic_mean"]
        ir = row["ir"]

        if abs(ic_mean) > 0.05 and abs(ir) > 0.5:
            status = "✅ 强有效"
        elif abs(ic_mean) > 0.03:
            status = "⚠️ 中等有效"
        else:
            status = "❌ 效果较弱"

        print(f"{row['factor_name']}: {status} (IC={ic_mean:.3f}, IR={ir:.3f})")

    return results_df


if __name__ == "__main__":
    # 注意：运行前需要先登录聚宽
    # auth('your_username', 'your_password')

    # results = run_factor_analysis()

    print("""
使用说明：
1. 首先需要安装聚宽SDK: pip install jqdatasdk
2. 登录聚宽账号: auth('username', 'password')
3. 运行分析: python factor_analysis.py

输出内容：
1. 各因子的IC均值、IC标准差、IR值
2. 因子相关性矩阵
3. 因子有效性判断
4. 分层收益分析

注意事项：
1. 分析需要较长时间（约30分钟）
2. 需要足够的聚宽API调用额度
3. 建议在非交易时间运行
    """)
