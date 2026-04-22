# 原文：https://www.joinquant.com/post/24321
# 标题：无杠杆，稳定盈利的etf轮动，06年开始3000%收益
# 作者：热爱大自然
# RiceQuant 移植版

import numpy as np


def init(context):
    # ETF 池：宽基、行业、商品、海外
    context.etf_pool = [
        '510050.XSHG',  # 上证50
        '510300.XSHG',  # 沪深300
        '510500.XSHG',  # 中证500
        '159915.XSHE',  # 创业板100
        '513100.XSHG',  # 纳指100
        '518880.XSHG',  # 黄金ETF
        '511010.XSHG',  # 国债ETF
        '159985.XSHE',  # 豆粕ETF
        '162411.XSHE',  # 华宝油气
        '513500.XSHG',  # 标普500
    ]

    context.bond_etf = '511010.XSHG'   # 避险资产：国债ETF
    context.index_code = '000300.XSHG'  # 市场择时基准：沪深300

    context.momentum_window = 20   # 动量回看窗口（交易日）
    context.ma_short = 20          # 短期均线
    context.ma_long = 60           # 长期均线
    context.top_n = 1              # 持仓 ETF 数量

    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    # ── 1. 市场择时：沪深300 短均线 < 长均线 → 空仓转债券 ──────────────────
    try:
        idx_closes = history_bars(context.index_code, context.ma_long + 1, '1d', 'close')
    except Exception:
        idx_closes = None

    in_bear = False
    if idx_closes is not None and len(idx_closes) >= context.ma_long:
        ma_s = np.mean(idx_closes[-context.ma_short:])
        ma_l = np.mean(idx_closes[-context.ma_long:])
        if ma_s < ma_l:
            in_bear = True

    if in_bear:
        _go_to_cash(context, bar_dict)
        return

    # ── 2. 计算每只 ETF 的动量得分（线性回归斜率 × R²） ──────────────────────
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.momentum_window + 1, '1d', 'close')
        except Exception:
            continue
        if closes is None or len(closes) < context.momentum_window:
            continue

        log_prices = np.log(closes[-context.momentum_window:])
        x = np.arange(len(log_prices))
        slope, intercept = np.polyfit(x, log_prices, 1)

        # R² 计算
        y_hat = slope * x + intercept
        ss_res = np.sum((log_prices - y_hat) ** 2)
        ss_tot = np.sum((log_prices - np.mean(log_prices)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        score = slope * r2
        if score > 0:
            scores[etf] = score

    # ── 3. 选出得分最高的 top_n 只 ETF ───────────────────────────────────────
    if not scores:
        # 无正动量标的，转债券避险
        _go_to_cash(context, bar_dict)
        return

    ranked = sorted(scores, key=lambda e: scores[e], reverse=True)
    target_etfs = set(ranked[:context.top_n])

    # ── 4. 卖出不在目标列表的持仓 ────────────────────────────────────────────
    for etf, pos in list(context.portfolio.positions.items()):
        if etf not in target_etfs and pos.quantity > 0:
            order_target_value(etf, 0)

    # ── 5. 等权买入目标 ETF ───────────────────────────────────────────────────
    weight = 1.0 / len(target_etfs)
    for etf in target_etfs:
        order_target_value(etf, context.portfolio.total_value * weight)


def _go_to_cash(context, bar_dict):
    """清仓非国债持仓，全仓买入国债 ETF。"""
    for etf, pos in list(context.portfolio.positions.items()):
        if etf != context.bond_etf and pos.quantity > 0:
            order_target_value(etf, 0)
    order_target_value(context.bond_etf, context.portfolio.total_value * 1.0)
