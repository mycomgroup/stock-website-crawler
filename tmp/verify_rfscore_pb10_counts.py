from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


START_DATE = "2022-01-01"
END_DATE = "2025-12-31"


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1
        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01
        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)
        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1
        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


def get_monthly_dates(start_date, end_date):
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    dates = []
    current_month = None
    for day in trade_days:
        if day.month != current_month:
            dates.append(day)
            current_month = day.month
    return dates


def get_universe(date):
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= date - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()
    return stocks


def calc_rfscore_frame(stocks, date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)

    basic = factor.basic.copy()
    basic["RFScore"] = factor.fscore

    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]

    basic = basic.join(val, how="left")
    basic = basic.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["RFScore", "pb_ratio"]
    )
    basic["pb_group"] = (
        pd.qcut(
            basic["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
        )
        + 1
    )

    return basic


# Main verification
print("验证 RFScore=7 且 PB10% 的股票数量")
print(f"测试期间: {START_DATE} 至 {END_DATE}")

dates = get_monthly_dates(START_DATE, END_DATE)
print(f"月度调仓次数: {len(dates)}")

counts = []
zero_count_months = 0
max_count = 0
max_count_date = None

for i in range(len(dates) - 1):
    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)

    stocks = get_universe(date)
    frame = calc_rfscore_frame(stocks, date_str)

    # Count stocks meeting both conditions
    qualified = frame[(frame["RFScore"] == 7) & (frame["pb_group"] == 1)]
    count = len(qualified)
    counts.append(count)

    if count == 0:
        zero_count_months += 1
    if count > max_count:
        max_count = count
        max_count_date = date_str

    # Print progress every 12 months
    if i % 12 == 0:
        print(f"进度: {i}/{len(dates) - 1} ({i / (len(dates) - 1) * 100:.1f}%)")

    # Print details for first few months and interesting months
    if i < 6 or count > 1 or count == 0:
        print(f"{date_str}: universe={len(stocks)}, RFScore=7&PB10%={count}")

print("\n" + "=" * 50)
print("统计结果")
print("=" * 50)
print(f"总月份: {len(counts)}")
print(f"平均股票数: {np.mean(counts):.2f}")
print(f"中位数股票数: {np.median(counts):.2f}")
print(f"最大股票数: {max_count} (发生在 {max_count_date})")
print(f"零股票月份: {zero_count_months} ({zero_count_months / len(counts) * 100:.1f}%)")
print(
    f"股票数≤1的月份: {sum(1 for c in counts if c <= 1)} ({sum(1 for c in counts if c <= 1) / len(counts) * 100:.1f}%)"
)

# Show distribution
unique_counts = sorted(set(counts))
print(f"\n股票数分布:")
for c in unique_counts:
    freq = counts.count(c)
    print(f"  {c}只股票: {freq}个月 ({freq / len(counts) * 100:.1f}%)")
