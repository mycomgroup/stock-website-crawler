# ffscore选股加rsrs择时 - RiceQuant版本
# 原文：https://www.joinquant.com/post/38552
# 作者：美吉姆优秀毕业代表
# 注：Piotroski F-Score 9项指标 + RSRS择时，沪深300成分股，持仓10只

import numpy as np
import pandas as pd


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_index = '000300.XSHG'
    context.hold_num = 10
    context.N = 18
    context.M = 300
    context.score_threshold = 0.7
    context.slope_series = []
    context.slope_initialized = False
    context.last_month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


# ─── RSRS 择时 ────────────────────────────────────────────────────────────────

def _init_slopes(context):
    total = context.N + context.M
    highs = history_bars('000300.XSHG', total, '1d', 'high')
    lows = history_bars('000300.XSHG', total, '1d', 'low')
    if highs is None or lows is None or len(highs) < total:
        return []
    result = []
    for i in range(context.M):
        _lows = lows[i: i + context.N]
        _highs = highs[i: i + context.N]
        slope, _ = np.polyfit(_lows, _highs, 1)
        result.append(slope)
    return result


def _rsrs_signal(context):
    highs = history_bars('000300.XSHG', context.N, '1d', 'high')
    lows = history_bars('000300.XSHG', context.N, '1d', 'low')
    if highs is None or lows is None or len(highs) < context.N:
        return 'KEEP'
    lows = lows
    highs = highs
    slope, intercept = np.polyfit(lows, highs, 1)
    context.slope_series.append(slope)
    series = context.slope_series[-context.M:]
    if len(series) < 2:
        return 'KEEP'
    mean = np.mean(series)
    std = np.std(series)
    if std == 0:
        return 'KEEP'
    fitted = slope * lows + intercept
    ss_res = np.sum((highs - fitted) ** 2)
    ss_tot = np.sum((highs - np.mean(highs)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    zscore = (series[-1] - mean) / std * r2
    if zscore > context.score_threshold:
        return 'BUY'
    if zscore < -context.score_threshold:
        return 'SELL'
    return 'KEEP'


# ─── F-Score 选股 ─────────────────────────────────────────────────────────────

FSCORE_FACTORS = [
    'roa',
    'operating_cash_flow',
    'inc_net_profit_year_on_year',
    'gross_profit_margin',
    'debt_to_asset_ratio',
    'turnover_ratio',
    'or_yoy',
    'net_profit',
    'circulating_market_cap',
]


def _calc_fscore(df_latest, df_prev):
    scores = pd.Series(0, index=df_latest.index, dtype=int)

    if 'roa' in df_latest.columns:
        scores += (df_latest['roa'] > 0).astype(int)

    if 'operating_cash_flow' in df_latest.columns:
        scores += (df_latest['operating_cash_flow'] > 0).astype(int)

    if 'inc_net_profit_year_on_year' in df_latest.columns:
        scores += (df_latest['inc_net_profit_year_on_year'] > 0).astype(int)

    if 'operating_cash_flow' in df_latest.columns and 'net_profit' in df_latest.columns:
        scores += (df_latest['operating_cash_flow'] > df_latest['net_profit']).astype(int)

    if 'debt_to_asset_ratio' in df_latest.columns and 'debt_to_asset_ratio' in df_prev.columns:
        common = df_latest.index.intersection(df_prev.index)
        mask = df_latest.loc[common, 'debt_to_asset_ratio'] < df_prev.loc[common, 'debt_to_asset_ratio']
        scores.loc[common] += mask.astype(int)

    if 'gross_profit_margin' in df_latest.columns:
        scores += (df_latest['gross_profit_margin'] > 0).astype(int)

    if 'or_yoy' in df_latest.columns:
        scores += (df_latest['or_yoy'] > 0).astype(int)

    if 'turnover_ratio' in df_latest.columns and 'turnover_ratio' in df_prev.columns:
        common = df_latest.index.intersection(df_prev.index)
        mask = df_latest.loc[common, 'turnover_ratio'] > df_prev.loc[common, 'turnover_ratio']
        scores.loc[common] += mask.astype(int)

    if 'circulating_market_cap' in df_latest.columns and 'circulating_market_cap' in df_prev.columns:
        common = df_latest.index.intersection(df_prev.index)
        mask = df_latest.loc[common, 'circulating_market_cap'] <= df_prev.loc[common, 'circulating_market_cap'] * 1.01
        scores.loc[common] += mask.astype(int)

    return scores


def get_stock_list(context):
    today = context.now.strftime('%Y-%m-%d')
    prev_date = context.now.date()
    stocks = index_components(context.stock_index)
    if not stocks:
        return []

    try:
        prev_date = context.now.date()
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['roa', 'inc_net_profit_year_on_year', 'gross_profit_margin', 'net_profit', 'operating_cash_flow', 'turnover_ratio'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df.head(400)
        candidates = df.index.tolist()
    except Exception:
        return []
    if df is None or len(df) == 0:
        return []

    df_latest = df.dropna(how='all')

    scores = _calc_fscore(df_latest, df_latest)  # df_prev_raw unavailable, use same df
    scores = scores.sort_values(ascending=False)

    return list(scores.index[: context.hold_num])


def trade(context, bar_dict):
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    signal = _rsrs_signal(context)

    if signal == 'SELL':
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    target = get_stock_list(context)
    if not target:
        return

    target = [s for s in target if s in bar_dict and bar_dict[s].is_trading]
    if not target:
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    w = 1.0 / len(target)
    for s in target:
        order_target_value(s, context.portfolio.total_value * w * 0.95)
