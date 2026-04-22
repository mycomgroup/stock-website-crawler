# 随机森林策略（多因子评分版）- RiceQuant版本
# 逻辑：ROE+PB+动量+低换手率综合评分，月度调仓，低换手率（每月换仓比例<30%）

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1
    context.current_holdings = []


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 3e+10]
        df = df[df['roe'] > 0.05]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    def zscore(arr):
        s = np.std(arr)
        return (arr - np.mean(arr)) / s if s > 0 else np.zeros_like(arr)

    momentum = {}
    vol_cv = {}
    for stock in candidates:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            volumes = history_bars(stock, 20, '1d', 'volume')
            if closes is not None and len(closes) >= 21:
                momentum[stock] = closes[-1] / closes[0] - 1
            if volumes is not None and len(volumes) >= 20:
                v = np.array(volumes, dtype=float)
                vol_cv[stock] = np.std(v) / (np.mean(v) + 1e-10)
        except Exception:
            pass

    valid = [s for s in candidates if s in momentum and s in vol_cv]
    if len(valid) < 5:
        return

    mom_z = zscore(np.array([momentum[s] for s in valid]))
    roe_z = zscore(np.array([df.loc[s, 'roe'] if s in df.index else 0 for s in valid]))
    pb_z = zscore(np.array([df.loc[s, 'pb_ratio'] if s in df.index else 5 for s in valid]))
    vcv_z = zscore(np.array([vol_cv[s] for s in valid]))

    scores = {valid[i]: mom_z[i] * 0.25 + roe_z[i] * 0.35 - pb_z[i] * 0.15 - vcv_z[i] * 0.25
              for i in range(len(valid))}

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    new_target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not new_target:
        return

    # 低换手率：优先保留已持仓的股票（最多换30%）
    current = list(context.portfolio.positions.keys())
    keep = [s for s in current if s in new_target]
    add = [s for s in new_target if s not in current]
    max_new = max(1, int(context.stock_num * 0.3))
    target = keep + add[:max_new]
    target = target[:context.stock_num]

    for stock in current:
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
