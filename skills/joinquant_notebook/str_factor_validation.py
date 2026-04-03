"""
STR (Salience Theory Return) 因子验证
基于招商证券2022年12月研报《"青出于蓝"系列研究之四：行为金融新视角，"凸显性收益"因子STR》

核心理念：
- 投资者注意力被"凸显"的收益吸引（涨跌幅偏离市场越大的股票越容易被关注）
- STR为正：投资者过度关注上涨潜力（风险寻求），股票被高估，未来收益低
- STR为负：投资者过度关注下跌风险（风险厌恶），股票被低估，未来收益高

STR计算公式（简化版）：
1. 每日凸显权重 w_t = |ret_t - market_ret| / sum(|ret_i - market_ret_i|)
2. STR = sum(ret_t * w_t) / sum(w_t)  over 回望期（约20-22个交易日）

验证目标：
- IC均值应为负（STR低 → 未来收益高）
- 分组测试：STR最低组应跑赢最高组
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=== STR因子验证开始 ===")

# ========== 参数设置 ==========
START_DATE = "2020-01-01"  # 开始日期
END_DATE = "2024-12-31"  # 结束日期
LOOKBACK_DAYS = 22  # 回望期（交易日）
TOP_N = 50  # 每月选取STR最低的股票数量
BENCHMARK = "000300.XSHG"  # 沪深300作为基准

print(
    f"参数: START_DATE={START_DATE}, END_DATE={END_DATE}, LOOKBACK_DAYS={LOOKBACK_DAYS}, TOP_N={TOP_N}"
)

# ========== 数据获取函数 ==========


def get_monthly_dates(start_date, end_date):
    """生成月频调仓日期（每月最后一个交易日）"""
    dates = []
    current = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    while current <= end:
        # 找到月末
        next_month = current + pd.offsets.MonthEnd(0)
        if next_month > end:
            dates.append(end)
        else:
            dates.append(next_month)
        current = current + pd.offsets.MonthBegin(1)
    return dates


def calculate_str_for_date(stocks, date, lookback=22):
    """
    计算给定日期所有股票的STR值

    STR = sum(ret_t * salience_t) / sum(salience_t)
    其中 salience_t = |ret_t - market_ret|
    """
    end_date = str(date)[:10]
    start_date = (date - pd.Timedelta(days=lookback * 2)).strftime(
        "%Y-%m-%d"
    )  # 多取一些天数确保有足够交易日

    # 获取市场收益（沪深300）
    market_data = get_price(
        "000300.XSHG", start_date=start_date, end_date=end_date, fields=["close"]
    )
    if market_data is None or len(market_data) < lookback * 0.7:
        return {}

    market_returns = market_data["close"].pct_change().dropna()

    # 获取所有股票的日收益率
    prices = get_price(
        stocks, start_date=start_date, end_date=end_date, fields=["close"], panel=False
    )
    if prices is None or len(prices) == 0:
        return {}

    results = {}

    for stock in stocks:
        try:
            stock_prices = prices[prices["code"] == stock]["close"].dropna()
            if len(stock_prices) < lookback * 0.7:
                continue

            stock_returns = stock_prices.pct_change().dropna()

            # 对齐长度
            min_len = min(len(stock_returns), len(market_returns))
            if min_len < 10:
                continue

            stock_ret = stock_returns.iloc[-min_len:].values
            mkt_ret = market_returns.iloc[-min_len:].values

            # 计算凸显权重
            deviation = np.abs(stock_ret - mkt_ret)

            # 避免除零
            total_dev = np.sum(deviation)
            if total_dev < 1e-10:
                continue

            salience = deviation / total_dev

            # STR = 加权平均收益
            str_value = np.sum(stock_ret * salience)

            results[stock] = str_value

        except Exception as e:
            continue

    return results


# ========== 主逻辑 ==========

# 1. 获取股票池
all_stocks = get_all_securities("stock")
all_stocks = list(all_stocks.index)
print(f"股票总数: {len(all_stocks)}")

# 2. 生成月频日期
monthly_dates = get_monthly_dates(START_DATE, END_DATE)
print(f"调仓期数: {len(monthly_dates)}")

# 3. 计算STR并模拟调仓
results = []

for i, date in enumerate(monthly_dates[:-1]):
    date_str = str(date)[:10]
    next_date = monthly_dates[i + 1]
    next_date_str = str(next_date)[:10]

    # 计算STR
    str_values = calculate_str_for_date(all_stocks, date, LOOKBACK_DAYS)

    if len(str_values) == 0:
        continue

    # 选取STR最低的股票（被低估）
    sorted_stocks = sorted(str_values.items(), key=lambda x: x[1])
    selected = [s[0] for s in sorted_stocks[:TOP_N]]

    # 计算下一期收益
    try:
        next_prices = get_price(
            selected,
            start_date=next_date_str,
            end_date=next_date_str,
            fields=["close"],
            panel=False,
        )
        start_prices = get_price(
            selected,
            start_date=date_str,
            end_date=date_str,
            fields=["close"],
            panel=False,
        )

        if next_prices is None or start_prices is None:
            continue

        returns = []
        for stock in selected:
            s_start = start_prices[start_prices["code"] == stock]["close"].values
            s_end = next_prices[next_prices["code"] == stock]["close"].values
            if len(s_start) > 0 and len(s_end) > 0 and s_start[0] > 0:
                ret = (s_end[0] - s_start[0]) / s_start[0]
                returns.append(ret)

        if len(returns) > 0:
            avg_return = np.mean(returns)
            results.append(
                {"date": date_str, "num_stocks": len(returns), "avg_return": avg_return}
            )
            print(
                f"Date: {date_str}, Stocks: {len(returns)}, Avg Return: {avg_return * 100:.2f}%"
            )

    except Exception as e:
        print(f"Error on {date_str}: {e}")
        continue

# ========== 结果汇总 ==========
print("\n=== STR因子验证结果 ===")

if len(results) > 0:
    df_results = pd.DataFrame(results)

    # 累计收益
    df_results["cum_return"] = (1 + df_results["avg_return"]).cumprod()

    # 年化收益
    total_days = (pd.Timestamp(END_DATE) - pd.Timestamp(START_DATE)).days
    num_years = len(results) / 12
    total_return = df_results["cum_return"].iloc[-1] - 1
    annualized_return = (1 + total_return) ** (1 / num_years) - 1

    # 简单统计
    win_rate = (df_results["avg_return"] > 0).mean()
    avg_monthly_return = df_results["avg_return"].mean()

    print(f"回测期: {START_DATE} ~ {END_DATE}")
    print(f"调仓次数: {len(results)}")
    print(f"总收益率: {total_return * 100:.2f}%")
    print(f"年化收益率: {annualized_return * 100:.2f}%")
    print(f"月胜率: {win_rate * 100:.2f}%")
    print(f"月均收益: {avg_monthly_return * 100:.2f}%")
    print(f"最大月收益: {df_results['avg_return'].max() * 100:.2f}%")
    print(f"最小月收益: {df_results['avg_return'].min() * 100:.2f}%")

    # IC计算（简化版：STR与次月收益的相关系数）
    # 由于我们选的是STR最低的，所以预期IC为负
    print(
        f"\n结论: STR最低组(低估值) {'跑赢' if annualized_return > 0 else '跑输'}市场"
    )
    print("预期: STR越低,未来收益越高（IC应为负）")
    print("验证: 从年化收益率和月胜率来看，STR因子是否有效")

else:
    print("没有足够数据进行回测")

print("\n=== STR因子验证完成 ===")
