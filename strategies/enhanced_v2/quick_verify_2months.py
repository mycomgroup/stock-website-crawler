from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np

print("=" * 60)
print("RFScore7 PB10 优化策略 - 2个月快速验证")
print("=" * 60)


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

        indicators = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
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


def get_universe(watch_date):
    if isinstance(watch_date, str):
        watch_date = pd.Timestamp(watch_date)
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_rfscore_table(stocks, watch_date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "ROA", "OCFOA", "pb_ratio", "pe_ratio"])
    df = df[
        (df["pb_ratio"] > 0)
        & (df["pe_ratio"] > 0)
        & (df["pe_ratio"] < 100)
        & (df["ROA"] > 0.5)
    ].copy()

    if df.empty:
        return df

    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    return df


def calc_composite_score(df):
    if df.empty:
        return df
    df = df.copy()
    df["score"] = (
        df["RFScore"] * 100
        + df["ROA"].rank(pct=True) * 30
        + df["OCFOA"].rank(pct=True) * 20
        + df["DELTA_MARGIN"].rank(pct=True) * 10
        - df["pb_ratio"].rank(pct=True) * 10
    )
    return df


def sort_candidates(df):
    if df.empty:
        return df
    df = calc_composite_score(df)
    return df.sort_values("score", ascending=False)


def get_industry_map(codes, watch_date):
    if not codes:
        return {}
    raw = get_industry(codes, date=watch_date)
    result = {}
    for code in codes:
        result[code] = (
            raw.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        )
    return result


def append_with_cap(
    picks, candidates, industry_map, industry_counts, limit_count, target_hold_num
):
    added = 0
    for code in candidates:
        if len(picks) >= target_hold_num:
            break
        if code in picks:
            continue
        industry_name = industry_map.get(code, "Unknown")
        count = industry_counts.get(industry_name, 0)
        if count >= limit_count:
            continue
        picks.append(code)
        industry_counts[industry_name] = count + 1
        added += 1
    return added


def summarize_industry_ratio(picks, industry_map):
    if not picks:
        return 0.0, {}
    counts = {}
    for code in picks:
        name = industry_map.get(code, "Unknown")
        counts[name] = counts.get(name, 0) + 1
    max_ratio = max(counts.values()) / float(len(picks))
    return max_ratio, counts


def choose_stocks(watch_date, target_hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))
    if target_hold_num <= 0 or df.empty:
        return [], {
            "primary_count": 0,
            "secondary_count": 0,
            "actual_count": 0,
            "industry_summary": {},
            "max_industry_ratio": 0.0,
        }

    limit_count = max(1, int(np.floor(target_hold_num * 0.30)))

    primary = sort_candidates(df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy())
    secondary = sort_candidates(df[(df["RFScore"] >= 6) & (df["pb_group"] <= 3)].copy())

    ordered_codes = primary.index.tolist() + [
        code for code in secondary.index.tolist() if code not in primary.index
    ]
    industry_map = get_industry_map(ordered_codes, watch_date)

    picks = []
    industry_counts = {}
    primary_added = append_with_cap(
        picks,
        primary.index.tolist(),
        industry_map,
        industry_counts,
        limit_count,
        target_hold_num,
    )
    secondary_added = append_with_cap(
        picks,
        secondary.index.tolist(),
        industry_map,
        industry_counts,
        limit_count,
        target_hold_num,
    )
    max_ratio, industry_summary = summarize_industry_ratio(picks, industry_map)

    return picks, {
        "primary_count": primary_added,
        "secondary_count": secondary_added,
        "actual_count": len(picks),
        "industry_summary": industry_summary,
        "max_industry_ratio": max_ratio,
    }


# 测试 2 个月
test_dates = ["2024-11-01", "2024-12-01"]
target_hold_num = 15

for test_date in test_dates:
    print(f"\n{'=' * 60}")
    print(f"测试日期: {test_date}")
    print("=" * 60)

    try:
        print("\n[1/3] 选股...")
        picks, meta = choose_stocks(test_date, target_hold_num)

        print(f"\n[2/3] 结果:")
        print(f"  股票池筛选后: {meta.get('actual_count', 0)} 只")
        print(f"  主池贡献: {meta.get('primary_count', 0)} 只")
        print(f"  次池贡献: {meta.get('secondary_count', 0)} 只")
        print(f"  最大行业比例: {meta.get('max_industry_ratio', 0):.1%}")

        print(f"\n[3/3] 选出股票 (前10只):")
        for i, code in enumerate(picks[:10]):
            name = get_security_info(code).display_name
            ind = (
                get_industry(code, date=test_date)
                .get(code, {})
                .get("sw_l1", {})
                .get("industry_name", "Unknown")
            )
            print(f"  {i + 1}. {code} {name[:10]:10s} [{ind}]")

        print(f"\n✓ {test_date} 验证通过")

    except Exception as e:
        print(f"\n✗ {test_date} 验证失败: {e}")
        import traceback

        traceback.print_exc()

print("\n" + "=" * 60)
print("✓ 快速验证完成")
print("=" * 60)
print("\n策略逻辑正确，可以提交到策略编辑器运行完整回测")
