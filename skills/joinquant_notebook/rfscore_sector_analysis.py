"""
RFScore PB10 历史行业分布分析脚本
用于抓取历史月度候选股票的行业分布数据
"""

from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json


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


def get_rfscore_candidates(trade_day):
    """获取指定日期的RFScore7 PB10候选股票"""
    trade_day_str = str(trade_day)

    # 获取中证800成分股
    hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
    zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
    stocks = [stock for stock in (hs300 | zz500) if not stock.startswith("688")]

    # 基础过滤
    sec = get_all_securities(types=["stock"], date=trade_day)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()

    # 排除ST
    is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 排除停牌
    paused = get_price(
        stocks, end_date=trade_day_str, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    if len(stocks) == 0:
        return pd.DataFrame()

    # 计算RFScore
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    # 获取估值
    val = get_valuation(
        stocks, end_date=trade_day_str, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

    # PB分组
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # 筛选RFScore=7且PB最低组
    df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()

    # 排序
    df = df.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )

    return df


def get_industry_distribution(codes, trade_day):
    """获取股票的行业分布"""
    if len(codes) == 0:
        return {}

    industry_counts = {}
    for code in codes:
        try:
            info = get_industry(code, date=trade_day)
            sw1 = info.get(code, {}).get("sw_l1", {})
            industry_name = sw1.get("industry_name", "未知")
            industry_counts[industry_name] = industry_counts.get(industry_name, 0) + 1
        except:
            industry_counts["未知"] = industry_counts.get("未知", 0) + 1

    return industry_counts


def get_valuation_stats(codes, trade_day):
    """获取估值统计"""
    if len(codes) == 0:
        return {}

    try:
        val = get_valuation(
            codes,
            end_date=str(trade_day),
            fields=["pb_ratio", "pe_ratio", "market_cap"],
            count=1,
        )
        val = val.drop_duplicates("code")

        return {
            "avg_pb": round(val["pb_ratio"].mean(), 4),
            "median_pb": round(val["pb_ratio"].median(), 4),
            "avg_pe": round(val["pe_ratio"].mean(), 4),
            "median_pe": round(val["pe_ratio"].median(), 4),
            "avg_market_cap": round(val["market_cap"].mean(), 2),
        }
    except:
        return {}


# 主程序
print("=" * 60)
print("RFScore PB10 历史行业分布分析")
print("=" * 60)
# 获取最近24个月的月度调仓日
today = datetime.now().date()
trade_days = get_trade_days(end_date=today, count=500)

# 选择每月最后一个交易日
monthly_dates = []
current_month = None
for day in reversed(trade_days):
    month_key = (day.year, day.month)
    if month_key != current_month:
        monthly_dates.append(day)
        current_month = month_key
    if len(monthly_dates) >= 24:
        break

monthly_dates = list(reversed(monthly_dates))
print(f"分析区间: {monthly_dates[0]} 至 {monthly_dates[-1]}")
print(f"共 {len(monthly_dates)} 个调仓月份")
print()

# 存储所有历史数据
all_history = []

# 遍历每个月度调仓日
for trade_day in monthly_dates:
    print(f"处理: {trade_day}")

    try:
        df = get_rfscore_candidates(trade_day)

        if len(df) == 0:
            print(f"  无候选股票")
            continue

        codes = df.index.tolist()

        # 获取行业分布
        industry_dist = get_industry_distribution(codes, trade_day)

        # 获取估值统计
        val_stats = get_valuation_stats(codes, trade_day)

        # 记录数据
        record = {
            "date": str(trade_day),
            "candidate_count": len(df),
            "industry_distribution": industry_dist,
            "valuation": val_stats,
            "top_5_stocks": codes[:5],
        }
        all_history.append(record)

        print(f"  候选数量: {len(df)}, 行业数: {len(industry_dist)}")

    except Exception as e:
        print(f"  错误: {e}")

print()
print("=" * 60)
print("分析完成")
print("=" * 60)

# 输出结果
result = {
    "analysis_period": {
        "start": str(monthly_dates[0]),
        "end": str(monthly_dates[-1]),
        "months": len(monthly_dates),
    },
    "monthly_data": all_history,
}

# 统计整体行业分布
all_industries = {}
for record in all_history:
    for industry, count in record["industry_distribution"].items():
        all_industries[industry] = all_industries.get(industry, 0) + count

# 按出现频率排序
sorted_industries = sorted(all_industries.items(), key=lambda x: x[1], reverse=True)

print("\n整体行业分布统计 (24个月累计):")
print("-" * 60)
total_count = sum(list(all_industries.values()))
for industry, count in sorted_industries[:15]:
    percentage = count / total_count * 100 if total_count > 0 else 0
    print(f"  {industry:20s}: {count:3d} ({percentage:5.1f}%)")

# 当前候选分析
current_day = monthly_dates[-1]
print(f"\n当前候选分析 ({current_day}):")
print("-" * 60)

current_df = get_rfscore_candidates(current_day)
if len(current_df) > 0:
    current_codes = current_df.index.tolist()
    current_industry = get_industry_distribution(current_codes, current_day)

    # 获取详细信息
    name_map = (
        get_all_securities(types=["stock"], date=current_day)
        .loc[current_codes, "display_name"]
        .to_dict()
    )

    print(f"候选数量: {len(current_df)}")
    print(f"\n行业分布:")
    for industry, count in sorted(
        current_industry.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = count / len(current_df) * 100
        print(f"  {industry:20s}: {count:2d} ({percentage:5.1f}%)")

    print(f"\nTop 10 候选股详情:")
    for i, code in enumerate(current_codes[:10], 1):
        name = name_map.get(code, "未知")
        pb = current_df.loc[code, "pb_ratio"]
        pe = current_df.loc[code, "pe_ratio"]
        info = get_industry(code, date=current_day)
        sw1 = info.get(code, {}).get("sw_l1", {})
        industry_name = sw1.get("industry_name", "未知")
        print(
            f"  {i:2d}. {code} {name:15s} PB={pb:5.2f} PE={pe:7.2f} [{industry_name}]"
        )

# 保存完整结果
output_json = json.dumps(result, ensure_ascii=False, indent=2)
print(f"\n\n完整JSON结果:\n{output_json}")
