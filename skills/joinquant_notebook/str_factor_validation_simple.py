"""
STR (Salience Theory Return) 因子验证 - 简化版
验证STR因子与股票未来收益的关系
"""

import pandas as pd
import numpy as np

print("=== STR因子验证(简化版)开始 ===")

# ========== 参数设置 ==========
TEST_DATE = "2023-06-30"  # 测试一个月的效果
LOOKBACK_DAYS = 22  # 回望期

print(f"测试日期: {TEST_DATE}, 回望期: {LOOKBACK_DAYS}天")

# ========== 获取股票池 ==========
# 使用沪深300成分股作为股票池
hs300 = get_index_stocks("000300.XSHG")
zz500 = get_index_stocks("000905.XSHG")
all_stocks = list(set(hs300 + zz500))
# 过滤ST - 使用get_extras获取ST状态
st_status = get_extras("is_st", stocks, end_date=TEST_DATE, count=1).iloc[-1]
stocks = [s for s in stocks if not st_status.get(s, False)]
print(f"股票池大小: {len(stocks)}")

# ========== 计算STR ==========
# STR = sum(ret_t * |ret_t - market_ret|) / sum(|ret_t - market_ret|)
# 简化：直接使用日收益率的加权平均，权重为偏离度


def calculate_str(stocks, date, lookback=22):
    """计算STR因子"""
    end_date = date
    start_date = (pd.Timestamp(date) - pd.Timedelta(days=lookback * 2)).strftime(
        "%Y-%m-%d"
    )

    # 获取市场收益（沪深300）
    market = get_price(
        "000300.XSHG", start_date=start_date, end_date=end_date, fields=["close"]
    )
    market_ret = market["close"].pct_change().dropna()

    # 获取股票价格
    prices = get_price(
        stocks, start_date=start_date, end_date=end_date, fields=["close"], panel=False
    )

    results = {}
    for stock in stocks:
        try:
            stock_prices = prices[prices["code"] == stock]["close"].dropna()
            stock_ret = stock_prices.pct_change().dropna()

            # 对齐
            min_len = min(len(stock_ret), len(market_ret))
            if min_len < 10:
                continue

            sret = stock_ret.iloc[-min_len:].values
            mret = market_ret.iloc[-min_len:].values

            # 偏离度
            deviation = np.abs(sret - mret)
            total_dev = np.sum(deviation)
            if total_dev < 1e-10:
                continue

            # STR
            str_val = np.sum(sret * deviation) / total_dev
            results[stock] = str_val
        except:
            continue

    return results


# 计算STR
str_values = calculate_str(stocks, TEST_DATE, LOOKBACK_DAYS)
print(f"成功计算STR的股票数: {len(str_values)}")

if len(str_values) == 0:
    print("STR计算失败")
    exit()

# ========== 分组测试 ==========
# 按STR值分成5组，看未来收益差异

# 获取下月收益
next_month_start = (pd.Timestamp(TEST_DATE) + pd.offsets.MonthBegin(1)).strftime(
    "%Y-%m-%d"
)
next_month_end = (pd.Timestamp(TEST_DATE) + pd.offsets.MonthEnd(1)).strftime("%Y-%m-%d")

start_prices = get_price(
    list(str_values.keys()),
    start_date=TEST_DATE,
    end_date=TEST_DATE,
    fields=["close"],
    panel=False,
)
end_prices = get_price(
    list(str_values.keys()),
    start_date=next_month_end,
    end_date=next_month_end,
    fields=["close"],
    panel=False,
)

# 计算收益
returns = {}
for stock in str_values.keys():
    try:
        s0 = start_prices[start_prices["code"] == stock]["close"].values[0]
        s1 = end_prices[end_prices["code"] == stock]["close"].values[0]
        returns[stock] = (s1 - s0) / s0
    except:
        continue

print(f"有收益数据的股票数: {len(returns)}")

# 分组
str_sorted = sorted(str_values.items(), key=lambda x: x[1])
n = len(str_sorted)
group_size = n // 5

groups = {}
for i in range(5):
    start_idx = i * group_size
    end_idx = (i + 1) * group_size if i < 4 else n
    group_stocks = [s[0] for s in str_sorted[start_idx:end_idx]]
    group_returns = [returns.get(s, 0) for s in group_stocks]
    groups[i] = {
        "name": f"Q{i + 1} (STR最高)",
        "avg_return": np.mean(group_returns),
        "count": len(group_returns),
    }

# 倒序显示（STR最低的在前）
print("\n=== STR分组测试结果 ===")
print(f"{'组别':<15} {'平均收益':>10} {'股票数':>8}")
for i in range(4, -1, -1):
    g = groups[i]
    print(f"{g['name']:<15} {g['avg_return'] * 100:>9.2f}% {g['count']:>8}")

# 统计
q1_return = groups[4]["avg_return"]  # STR最低组
q5_return = groups[0]["avg_return"]  # STR最高组
spread = q1_return - q5_return

print(f"\n多空组合收益: {spread * 100:.2f}%")
print(
    f"STR最低组 vs 最高组: {'STR低组跑赢' if q1_return > q5_return else 'STR高组跑赢'}"
)

# 计算IC（简化）
str_list = [
    (s, str_values[s], returns.get(s, 0)) for s in str_values.keys() if s in returns
]
if len(str_list) > 10:
    ic = np.corrcoef([x[1] for x in str_list], [x[2] for x in str_list])[0, 1]
    print(f"STR与未来收益的相关系数(IC): {ic:.4f}")
    print(f"预期IC为负（STR低→收益高）: {'✓ 符合预期' if ic < 0 else '✗ 不符合预期'}")

print("\n=== 验证结论 ===")
print("STR因子原理：投资者对'凸显'的收益（如涨停、跌停）反应过度")
print("STR为正：涨势凸显 → 过度乐观 → 未来收益低（动量反转）")
print("STR为负：跌势凸显 → 过度悲观 → 未来收益高（均值回归）")
