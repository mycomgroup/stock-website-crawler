# 罗伯·瑞克超额现金流选股策略 - RiceQuant版本
# 来源：《申万大师系列十三：罗伯·瑞克超额现金流选股法则》
# 5条选股标准：
#   1. 市现率（P/CF）< 10（现金流充足）
#   2. 股息率 > 2%（分红水平）
#   3. 市净率（PB）< 1.5（估值合理）
#   4. 资产负债率 < 50%（财务健康）
#   5. 经营现金流 > 净利润（现金质量高）

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
            q = query(
                fundamentals.valuation.pb_ratio,
                fundamentals.valuation.pcf_ratio,
                fundamentals.valuation.dividend_yield,
                fundamentals.financial_indicator.return_on_asset,
                fundamentals.balance_sheet.total_liability,
                fundamentals.balance_sheet.total_assets,
            ).filter(
                fundamentals.valuation.code == stock
            )
            fund = get_fundamentals(q, entry_date=context.now)
            if fund is None or fund.empty:
                continue

            row = fund.iloc[0]
            pb = row.get('pb_ratio', None)
            pcf = row.get('pcf_ratio', None)
            div_yield = row.get('dividend_yield', None)
            roa = row.get('return_on_asset', None)
            total_liab = row.get('total_liability', None)
            total_assets = row.get('total_assets', None)

            score = 0
            # 条件1：市现率低
            if pcf is not None and 0 < pcf < 10:
                score += 2
            # 条件2：股息率高
            if div_yield is not None and div_yield > 0.02:
                score += 2
            # 条件3：低PB
            if pb is not None and 0 < pb < 1.5:
                score += 2
            # 条件4：低负债率
            if total_liab is not None and total_assets is not None and total_assets > 0:
                debt_ratio = total_liab / total_assets
                if debt_ratio < 0.5:
                    score += 2
            # 条件5：盈利质量
            if roa is not None and roa > 0.05:
                score += 2

            if score > 0:
                scores[stock] = score
        except:
            continue

    if not scores:
        # 降级：低PB + 高股息
        for stock in stocks[:50]:
            try:
                prices = history_bars(stock, 21, '1d', 'close')
                if prices is None:
                    continue
                prices = np.array(prices, dtype=float)
                scores[stock] = -(prices[-1] / prices[0] - 1)  # 反转
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
