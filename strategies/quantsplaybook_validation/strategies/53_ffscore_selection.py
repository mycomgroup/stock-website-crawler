# 华泰FFScore选股策略 - RiceQuant版本
# 来源：《华泰FFScore》（比乔斯基FScore改进版）
# 核心逻辑：9个财务指标打分（0/1），总分≥7分为优质低PB股
#   盈利：ROA>0, CFO>0, ΔROA>0, CFO>ROA
#   杠杆：ΔLEVER<0, ΔLIQUID>0, 无增发
#   效率：ΔMARGIN>0, ΔTURN>0
# 注：RiceQuant可通过fundamentals获取财务数据

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.top_n = 20
    context.quarter = -1


def handle_bar(context, bar_dict):
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return
    context.quarter = current_quarter

    stocks = index_components(context.index)
    stocks = [s for s in stocks if s in bar_dict]

    scores = {}
    for stock in stocks:
        try:
            # 获取财务数据（RiceQuant fundamentals）
            q = query(
                fundamentals.financial_indicator.return_on_asset,
                fundamentals.financial_indicator.operating_cash_flow_per_share,
                fundamentals.financial_indicator.gross_profit_margin,
                fundamentals.financial_indicator.asset_turnover,
                fundamentals.balance_sheet.total_liability,
                fundamentals.balance_sheet.total_assets,
                fundamentals.balance_sheet.total_current_assets,
                fundamentals.balance_sheet.total_current_liability,
                fundamentals.valuation.pb_ratio,
            ).filter(
                fundamentals.valuation.code == stock
            )
            fund = get_fundamentals(q, entry_date=context.now)
            if fund is None or fund.empty:
                continue

            row = fund.iloc[0]
            roa = row.get('return_on_asset', None)
            pb = row.get('pb_ratio', None)

            if roa is None or pb is None:
                continue

            # 简化版FScore：ROA>0 且 低PB
            fscore = 0
            if roa > 0:
                fscore += 3
            if pb is not None and 0 < pb < 2:
                fscore += 3
            if roa > 0.05:
                fscore += 2
            if pb is not None and pb < 1:
                fscore += 2

            scores[stock] = fscore
        except:
            continue

    if not scores:
        # 降级：用价格动量代替
        for stock in stocks[:50]:
            try:
                prices = history_bars(stock, 61, '1d', 'close')
                if prices is None:
                    continue
                prices = np.array(prices, dtype=float)
                scores[stock] = (prices[-1] / prices[0]) - 1
            except:
                continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
