"""
RFScore7 PB10 Optimized V3
- 市场状态控制：接入 strategy_kits.signals.regime_filters.run_regime_gate（四状态路由器）
- 股票池过滤：接入 strategy_kits.universe.stock_pool_filters.apply_filters
- 选股/打分/配仓逻辑保持不变，保持 JoinQuant 平台兼容
"""
from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
try:
    import sys as _sys
    _SK_ROOT = "/Users/fengzhi/Downloads/git/testlixingren/skills"
    if _SK_ROOT not in _sys.path:
        _sys.path.insert(0, _SK_ROOT)
    from strategy_kits.signals.regime_filters import run_regime_gate, RegimeState
    from strategy_kits.universe.stock_pool_filters import apply_filters
    _SK_AVAILABLE = True
except Exception:
    _SK_AVAILABLE = False


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


# ── RFScore 因子定义（不变）──────────────────────────────────────────────────

class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa", "roa_4",
        "net_operate_cash_flow", "net_operate_cash_flow_1",
        "net_operate_cash_flow_2", "net_operate_cash_flow_3",
        "total_assets", "total_assets_1", "total_assets_2",
        "total_assets_3", "total_assets_4", "total_assets_5",
        "total_non_current_liability", "total_non_current_liability_1",
        "gross_profit_margin", "gross_profit_margin_4",
        "operating_revenue", "operating_revenue_4",
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
            data["total_assets"] + data["total_assets_1"]
            + data["total_assets_2"] + data["total_assets_3"]
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

        indicators = (roa, delta_roa, ocfoa, accrual, delta_leveler, delta_margin, delta_turn)
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA", "DELTA_ROA", "OCFOA", "ACCRUAL",
            "DELTA_LEVELER", "DELTA_MARGIN", "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


# ── 初始化 ────────────────────────────────────────────────────────────────────

def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.release_name = "RFScore7 PB10 Optimized V3"
    g.ipo_days = 180
    g.primary_pb_group = 1
    g.secondary_pb_group = 3
    g.max_pe_ratio = 100
    g.min_roa = 0.5
    g.industry_cap_ratio = 0.30
    g.max_single_ratio = 0.10
    g.stop_loss_ratio = -0.15

    # 持仓数：四状态路由器映射
    # ALLOWED -> normal, REDUCE -> mid, WARNING -> weak, HOLD -> stop
    g.hold_num_normal = 15
    g.hold_num_mid = 12
    g.hold_num_weak = 10
    g.hold_num_stop = 0

    # 宽度阈值（fallback：strategy_kits 不可用时使用）
    g.breadth_normal = 0.35
    g.breadth_reduce = 0.25
    g.breadth_stop = 0.15

    g.last_market_state = {}
    g.last_selection = {
        "target_hold_num": 0,
        "actual_hold_num": 0,
        "primary_count": 0,
        "secondary_count": 0,
        "cash_ratio": 1.0,
        "max_industry_ratio": 0.0,
        "stop_loss_count": 0,
        "regime_state": "unknown",
    }

    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(record_market_state, time="14:50", reference_security="000300.XSHG")


# ── 股票池构建 ────────────────────────────────────────────────────────────────

def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


# ── 市场状态：优先 regime_gate，fallback 原始宽度逻辑 ─────────────────────────

def calc_market_state_raw(watch_date):
    """原始宽度+趋势计算（fallback）"""
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)
    prices = get_price(hs300, end_date=watch_date, count=20, fields=["close"], panel=False)
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
    idx_close = float(idx["close"].iloc[-1])
    idx_ma20 = float(idx["close"].mean())
    trend_on = idx_close > idx_ma20

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "idx_close": idx_close,
        "idx_ma20": idx_ma20,
    }


def calc_regime_state(watch_date):
    """
    优先使用 strategy_kits.regime_filters.run_regime_gate 计算四状态。
    若 strategy_kits 不可用，fallback 到原始宽度逻辑并映射到 RegimeState 字符串。

    Returns
    -------
    regime_str : str  ("ALLOWED" / "REDUCE" / "WARNING" / "HOLD")
    raw_state  : dict  原始指标（供 record 使用）
    """
    raw = calc_market_state_raw(watch_date)

    if _SK_AVAILABLE:
        try:
            # 构造 market_data：strategy_kits 需要 index-date DataFrame
            idx_df = get_price(
                "000300.XSHG",
                end_date=watch_date,
                count=60,
                fields=["open", "high", "low", "close", "volume"],
            )
            idx_df.index = pd.to_datetime(idx_df.index)

            # 构造 breadth_data：全市场个股收盘价（用于宽度计算）
            hs300 = get_index_stocks("000300.XSHG", date=watch_date)
            breadth_prices = get_price(
                hs300, end_date=watch_date, count=20, fields=["close"], panel=False
            )
            breadth_df = breadth_prices.pivot(
                index="time", columns="code", values="close"
            )
            breadth_df.index = pd.to_datetime(breadth_df.index)

            gate_output = run_regime_gate(
                market_data=idx_df,
                breadth_data=breadth_df,
                date=str(watch_date),
            )
            regime_str = gate_output.regime_state.value.upper()
            # 统一映射：regime_gate 返回 allowed/reduce/hold/warning
            _REGIME_MAP = {
                "ALLOWED": "ALLOWED",
                "REDUCE": "REDUCE",
                "HOLD": "HOLD",
                "WARNING": "WARNING",
            }
            regime_str = _REGIME_MAP.get(regime_str, "WARNING")
            raw["regime_state"] = regime_str
            raw["regime_source"] = "regime_gate"
            return regime_str, raw
        except Exception as e:
            log.warn("regime_gate failed, fallback to breadth: %s" % str(e))

    # fallback：原始宽度逻辑映射到四状态
    breadth = raw["breadth"]
    trend_on = raw["trend_on"]
    if breadth < g.breadth_stop:
        regime_str = "HOLD"
    elif breadth < g.breadth_reduce:
        regime_str = "WARNING"
    elif breadth < g.breadth_normal and not trend_on:
        regime_str = "REDUCE"
    else:
        regime_str = "ALLOWED"

    raw["regime_state"] = regime_str
    raw["regime_source"] = "breadth_fallback"
    return regime_str, raw


def get_target_hold_num(regime_str):
    """四状态 -> 目标持仓数"""
    mapping = {
        "ALLOWED": g.hold_num_normal,
        "REDUCE": g.hold_num_mid,
        "WARNING": g.hold_num_weak,
        "HOLD": g.hold_num_stop,
    }
    return mapping.get(regime_str, g.hold_num_weak)


# ── 打分与选股 ────────────────────────────────────────────────────────────────

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
        & (df["pe_ratio"] < g.max_pe_ratio)
        & (df["ROA"] > g.min_roa)
    ].copy()

    if df.empty:
        return df

    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
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
        result[code] = raw.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
    return result


def append_with_cap(picks, candidates, industry_map, industry_counts, limit_count, target_hold_num):
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
            "primary_count": 0, "secondary_count": 0,
            "actual_count": 0, "industry_summary": {}, "max_industry_ratio": 0.0,
        }

    limit_count = max(1, int(np.floor(target_hold_num * g.industry_cap_ratio)))

    primary = sort_candidates(
        df[(df["RFScore"] == 7) & (df["pb_group"] == g.primary_pb_group)].copy()
    )
    secondary = sort_candidates(
        df[(df["RFScore"] >= 6) & (df["pb_group"] <= g.secondary_pb_group)].copy()
    )

    ordered_codes = primary.index.tolist() + [
        code for code in secondary.index.tolist() if code not in primary.index
    ]
    industry_map = get_industry_map(ordered_codes, watch_date)

    picks = []
    industry_counts = {}
    primary_added = append_with_cap(
        picks, primary.index.tolist(), industry_map, industry_counts, limit_count, target_hold_num
    )
    secondary_added = append_with_cap(
        picks, secondary.index.tolist(), industry_map, industry_counts, limit_count, target_hold_num
    )
    max_ratio, industry_summary = summarize_industry_ratio(picks, industry_map)

    return picks, {
        "primary_count": primary_added,
        "secondary_count": secondary_added,
        "actual_count": len(picks),
        "industry_summary": industry_summary,
        "max_industry_ratio": max_ratio,
    }


# ── 买入过滤：优先 apply_filters，fallback 原始逻辑 ───────────────────────────

def filter_buyable(context, stocks):
    """
    优先使用 strategy_kits.universe.stock_pool_filters.apply_filters。
    若不可用，fallback 到原始 current_data 逐股检查。
    """
    if _SK_AVAILABLE and stocks:
        try:
            watch_date = context.current_dt.date()
            result = apply_filters(
                base_universe=stocks,
                date=watch_date,
                filter_config={
                    "st": {"enabled": True},
                    "paused": {"enabled": True},
                    "limitup": {"enabled": True},
                    "limitdown": {"enabled": True},
                    "kcbj": {"enabled": False},   # 已在 get_universe 过滤 688
                    "new_stock": {"enabled": False},  # 已在 get_universe 过滤 ipo_days
                },
                positions=list(context.portfolio.positions.keys()),
            )
            return result.filtered_universe
        except Exception as e:
            log.warn("apply_filters failed, fallback: %s" % str(e))

    # fallback：原始逐股检查
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused:
            continue
        if current_data[stock].is_st:
            continue
        if (
            "ST" in current_data[stock].name
            or "*" in current_data[stock].name
            or "退" in current_data[stock].name
        ):
            continue
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        if last_price <= current_data[stock].low_limit * 1.005:
            continue
        buyable.append(stock)
    return buyable


# ── 止损检查（不变）─────────────────────────────────────────────────────────

def check_stop_loss(context):
    current_positions = list(context.portfolio.positions.keys())
    stop_loss_stocks = []
    for stock in current_positions:
        pos = context.portfolio.positions[stock]
        if pos.price > 0 and pos.avg_cost > 0:
            pnl_ratio = (pos.price - pos.avg_cost) / pos.avg_cost
            if pnl_ratio < g.stop_loss_ratio:
                stop_loss_stocks.append(stock)
    return stop_loss_stocks


# ── 调仓主逻辑 ────────────────────────────────────────────────────────────────

def rebalance(context):
    watch_date = context.previous_date

    # 1. 市场状态（四状态路由器）
    regime_str, raw_state = calc_regime_state(watch_date)
    g.last_market_state = raw_state

    # 2. 止损
    stop_loss_stocks = check_stop_loss(context)
    for stock in stop_loss_stocks:
        order_target_value(stock, 0)
        log.info("stop loss: %s" % stock)

    # 3. 目标持仓数
    target_hold_num = get_target_hold_num(regime_str)

    if target_hold_num <= 0:
        target_stocks = []
        meta = {
            "primary_count": 0, "secondary_count": 0,
            "actual_count": 0, "industry_summary": {}, "max_industry_ratio": 0.0,
        }
    else:
        target_stocks, meta = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)
        meta["actual_count"] = len(target_stocks)
        if target_stocks:
            industry_map = get_industry_map(target_stocks, watch_date)
            max_ratio, industry_summary = summarize_industry_ratio(target_stocks, industry_map)
            meta["industry_summary"] = industry_summary
            meta["max_industry_ratio"] = max_ratio
        else:
            meta["industry_summary"] = {}
            meta["max_industry_ratio"] = 0.0

    cash_ratio = 1.0
    if target_hold_num > 0:
        cash_ratio = max(0.0, 1.0 - len(target_stocks) / float(target_hold_num))

    g.last_selection = {
        "target_hold_num": target_hold_num,
        "actual_hold_num": len(target_stocks),
        "primary_count": meta["primary_count"],
        "secondary_count": meta["secondary_count"],
        "cash_ratio": cash_ratio,
        "max_industry_ratio": meta["max_industry_ratio"],
        "stop_loss_count": len(stop_loss_stocks),
        "regime_state": regime_str,
    }

    log.info(
        "release=%s watch_date=%s regime=%s(src=%s) breadth=%.3f trend_on=%s "
        "target_hold_num=%s actual_hold_num=%s primary=%s secondary=%s "
        "cash_ratio=%.2f stop_loss=%s"
        % (
            g.release_name,
            str(watch_date),
            regime_str,
            raw_state.get("regime_source", "?"),
            raw_state.get("breadth", 0.0),
            str(raw_state.get("trend_on", False)),
            str(target_hold_num),
            str(len(target_stocks)),
            str(meta["primary_count"]),
            str(meta["secondary_count"]),
            cash_ratio,
            str(len(stop_loss_stocks)),
        )
    )

    # 4. 清仓不在目标列表的持仓
    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    # 5. 等额建仓（单股上限 max_single_ratio）
    current_data = get_current_data()
    total_value = context.portfolio.total_value
    per_stock_value = total_value / float(len(target_stocks))
    max_single_value = total_value * g.max_single_ratio
    actual_value = min(per_stock_value, max_single_value)

    for stock in target_stocks:
        price = current_data[stock].last_price
        if price <= 0:
            continue
        target_amount = int(actual_value / price / 100) * 100
        if target_amount < 100:
            continue
        order_target(stock, target_amount)


# ── 每日记录 ──────────────────────────────────────────────────────────────────

def record_market_state(context):
    watch_date = context.previous_date
    regime_str, state = calc_regime_state(watch_date)
    record(
        breadth=state.get("breadth", 0.0),
        trend_on=1 if state.get("trend_on", False) else 0,
        hs300_close=state.get("idx_close", 0.0),
        hs300_ma20=state.get("idx_ma20", 0.0),
        regime_state_code={"ALLOWED": 3, "REDUCE": 2, "WARNING": 1, "HOLD": 0}.get(regime_str, 1),
        target_hold_num=g.last_selection.get("target_hold_num", 0),
        actual_hold_num=g.last_selection.get("actual_hold_num", 0),
        primary_count=g.last_selection.get("primary_count", 0),
        secondary_count=g.last_selection.get("secondary_count", 0),
        cash_ratio=g.last_selection.get("cash_ratio", 1.0),
        max_industry_ratio=g.last_selection.get("max_industry_ratio", 0.0),
        stop_loss_count=g.last_selection.get("stop_loss_count", 0),
    )
