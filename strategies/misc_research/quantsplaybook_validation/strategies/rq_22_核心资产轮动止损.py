# 带止损的核心资产轮动策略 - RiceQuant版本
# 原文：带上止损的核心资产轮动才更安心，低回撤，高收益率
# 作者：养家大哥
# 原文：https://www.joinquant.com/post/47966
# 逻辑：4只核心ETF按动量评分轮动，加入止损逻辑

import numpy as np
import pandas as pd


ETF_POOL = [
    '518880.XSHG',  # 黄金ETF
    '513100.XSHG',  # 纳指100
    '159915.XSHE',  # 创业板100
    '510330.XSHG',  # 沪深300ETF华夏（原上证180ETF已退市）
]


def init(context):
    context.etf_pool = ETF_POOL
    context.m_days = 25
    context.etf_pre = None
    scheduler.run_daily(trade, time_rule=market_open(minute=30))



def handle_bar(context, bar_dict):
    pass

def get_rank(context):
    score_list = []
    valid_etfs = []
    for etf in context.etf_pool:
        try:
            prices = history_bars(etf, context.m_days, '1d', 'close')
            if prices is None or len(prices) < context.m_days:
                continue
            y = np.log(np.array(prices, dtype=float))
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            annualized = np.exp(slope * 250) - 1
            y_hat = slope * x + intercept
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = (len(y) - 1) * np.var(y, ddof=1)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            score_list.append(annualized * r2)
            valid_etfs.append(etf)
        except Exception:
            continue

    if not valid_etfs:
        return []
    df = pd.DataFrame({'score': score_list}, index=valid_etfs)
    return df.sort_values('score', ascending=False).index.tolist()


def evaluate_hold_worth(context, etf):
    """判断持仓是否值得继续持有（止损检查）"""
    try:
        prices = history_bars(etf, 2, '1d', 'close')
        if prices is None or len(prices) < 2:
            return True
        cur2yes = prices[-1] / prices[-2]
        # 单日跌幅超过4%触发止损
        return cur2yes > 0.96
    except Exception:
        return True


def trade(context, bar_dict):
    rank = get_rank(context)
    if not rank:
        return

    sel_etf = rank[0]
    hold_list = list(context.portfolio.positions.keys())
    hold_etf = hold_list[0] if hold_list else None

    hold_worth = evaluate_hold_worth(context, hold_etf) if hold_etf else False

    if hold_etf is not None:
        context.etf_pre = hold_etf
        if sel_etf not in hold_list:
            order_target_value(hold_etf, 0)
        elif not hold_worth:
            order_target_value(hold_etf, 0)

    if sel_etf != context.etf_pre:
        order_target_value(sel_etf, context.portfolio.cash * 0.95)
    elif len(hold_list) == 0 and sel_etf == context.etf_pre:
        # 止损后恢复买入
        prices = history_bars(sel_etf, 4, '1d', 'close')
        if prices is not None and len(prices) >= 4:
            cur_p = prices[-1]
            mean4 = np.mean(prices[-4:])
            if cur_p >= mean4:
                order_target_value(sel_etf, context.portfolio.cash * 0.95)
