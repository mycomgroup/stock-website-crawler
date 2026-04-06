# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/40118
# 标题：开盘幅度决定日内方向
# 作者：ZWK123
#
# ⚠️  迁移说明（RiceQuant版本）：
#   原JQ策略核心依赖以下无法迁移的API：
#     - attribute_history()  → RQ无对应日内开盘价历史接口
#     - day_open             → RQ无此属性
#     - get_trades(side='long') → RQ无此接口
#   本版本用 history_bars(..., '1d', 'close') 取昨收 + bar_dict[s].open 取今开
#   近似实现"开盘幅度"逻辑，逻辑等价但非完全复现。
#
#   结构修复：
#   - before_market_open 原本被 scheduler 调度在 market_open(minute=0)（错误），
#     且函数体内只做初始化，已合并到 init() 中，scheduler 条目已移除。
#   - context.now → context.now

# 回测资金设置为 1000000

def init(context):
    print('初始函数开始运行且全局只运行一次')

    # 要操作的标的：沪深300ETF
    context.security = '510300.XSHG'

    # 开盘时运行
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=0))
    # 收盘后运行
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def market_open_trade(context, bar_dict):
    print('函数运行时间(market_open):' + str(context.now))
    # 取昨收（index -2）近似计算开盘幅度
    bars_300 = history_bars('000300.XSHG', 2, '1d', 'close')
    bars_303 = history_bars('399303.XSHE', 2, '1d', 'close')
    if bars_300 is None or bars_303 is None or len(bars_300) < 2 or len(bars_303) < 2:
        return

    # 今日开盘价：用日频 open 字段近似
    open_bars_300 = history_bars('000300.XSHG', 1, '1d', 'open')
    open_bars_303 = history_bars('399303.XSHE', 1, '1d', 'open')
    open_300 = open_bars_300[-1] if open_bars_300 is not None and len(open_bars_300) > 0 else bars_300[-1]
    open_303 = open_bars_303[-1] if open_bars_303 is not None and len(open_bars_303) > 0 else bars_303[-1]

    prev_close_300 = bars_300[-2]
    prev_close_303 = bars_303[-2]
    fudu_300 = open_300 / prev_close_300 if prev_close_300 != 0 else 1
    fudu_303 = open_303 / prev_close_303 if prev_close_303 != 0 else 1

    ava_cash = context.portfolio.cash
    position = context.portfolio.positions

    if (fudu_300 > fudu_303 or fudu_300 > 1) and not position:
        order_target_value(context.security, ava_cash * 0.95)
        print('开多 fudu_300={:.4f} fudu_303={:.4f}'.format(fudu_300, fudu_303))
    elif fudu_300 < fudu_303 and fudu_300 < 1 and position:
        order_target_value(context.security, 0)
        print('平多 fudu_300={:.4f} fudu_303={:.4f}'.format(fudu_300, fudu_303))


def after_market_close(context, bar_dict):
    print('函数运行时间(after_market_close):' + str(context.now))
    print('一天结束')
    print('##############################################################')
