# 风险及免责提示：该策略由聚宽用户分享，仅供学习交流使用。
# 克隆自聚宽文章：https://www.joinquant.com/post/30551
# 标题：敢于直接实盘的—八仙过海V2
# 作者：Funine
# RiceQuant 移植版：删除 talib/jqdata 依赖，用 numpy 手动计算均线

import numpy as np

# ETF 标的列表（主动基金 + 宽基ETF）
ETF_TARGETS = [
    '162605.XSHE',  # 景顺鼎益
    '161903.XSHE',  # 万家
    '161005.XSHE',  # 富国天惠
    '163417.XSHE',  # 兴全合一
    '163402.XSHE',  # 兴全趋势
    '163415.XSHE',  # 兴全模式
    '501054.XSHG',  # 东征睿泽
    '162703.XSHE',  # 广发小盘
]

MONEY_FUND = '511880.XSHG'  # 空仓时持有的货币基金
LAG = 60                     # 历史数据天数（均线最长60日）


def init(context):
    context.etf_list = ETF_TARGETS
    context.active_etfs = []   # 过滤后的可交易 ETF
    context.lag = LAG

    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(get_signal, time_rule=market_close(minute=30))



def handle_bar(context, bar_dict):
    pass

def before_market_open(context, bar_dict):
    """盘前：过滤上市不足60天的ETF"""
    active = []
    for etf in context.etf_list:
        try:
            instrument = instruments(etf)
            # 上市天数需超过 lag，保证均线数据充足
            listed_days = (context.now - instrument.listed_date).days
            if listed_days >= context.lag:
                active.append(etf)
        except Exception as e:
            print(f'[before_market_open] 跳过 {etf}，原因：{e}')
    context.active_etfs = active
    print(f'[before_market_open] 可交易ETF数量：{len(active)}')


def _ma_score(etf, context, bar_dict):
    """
    计算单个ETF的均线得分。
    价格 > MA5  +0.30
    价格 > MA10 +0.25
    价格 > MA20 +0.20
    价格 > MA30 +0.15
    价格 > MA60 +0.10
    返回值范围 0~1，代表目标仓位比例。
    """
    try:
        closes = history_bars(etf, context.lag, '1d', 'close')
        if closes is None or len(closes) < context.lag:
            return 0.0
        current_price = bar_dict[etf].close
        score = 0.0
        if current_price > np.mean(closes[-5:]):   score += 0.30
        if current_price > np.mean(closes[-10:]):  score += 0.25
        if current_price > np.mean(closes[-20:]):  score += 0.20
        if current_price > np.mean(closes[-30:]):  score += 0.15
        if current_price > np.mean(closes[-60:]):  score += 0.10
        return score
    except Exception as e:
        print(f'[_ma_score] {etf} 计算失败：{e}')
        return 0.0


def get_signal(context, bar_dict):
    """14:30 计算均线得分，按得分调仓"""
    total_value = context.portfolio.total_value

    scores = {}
    for etf in context.active_etfs:
        scores[etf] = _ma_score(etf, context, bar_dict)

    print(f'[get_signal] 均线得分：{scores}')

    # 清仓得分为0或不在列表的持仓
    for code in list(context.portfolio.positions.keys()):
        if code == MONEY_FUND:
            continue
        if code not in scores or scores[code] == 0.0:
            order_target_value(code, 0)
            print(f'[get_signal] 清仓 {code}')

    total_score = sum(scores.values())

    if total_score == 0:
        # 全部空仓，持货币基金
        if MONEY_FUND in bar_dict:
            order_target_value(MONEY_FUND, total_value * 0.95)
    else:
        # 卖出货币基金
        if MONEY_FUND in context.portfolio.positions:
            order_target_value(MONEY_FUND, 0)
        # 按得分比例分配仓位
        for etf, score in scores.items():
            if score == 0.0:
                continue
            target_value = total_value * (score / total_score) * 0.95
            order_target_value(etf, target_value)
            print(f'[get_signal] {etf} 得分={score:.2f} 目标金额={target_value:.0f}')
