# 短线策略-2022年两个半月收益45%-无未来函数 - RiceQuant版本
# 原文：https://www.joinquant.com/post/36975
# 作者：zk001
# 逻辑：全A股（排除688/4/8/ST），MACD金叉 + 量能放大 + 价格在MA20之上
#       次日开盘买入，持仓3-5天或止损-5%，持仓5只，每日检查

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_num = 5
    context.stop_loss = 0.05       # 止损 -5%
    context.max_hold_days = 5      # 最大持仓天数
    context.buy_price = {}
    context.hold_days = {}
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


# ── EMA & MACD（numpy）────────────────────────────────────────────────────────

def _ema(arr, period):
    k = 2.0 / (period + 1)
    out = np.empty(len(arr))
    out[0] = arr[0]
    for i in range(1, len(arr)):
        out[i] = arr[i] * k + out[i - 1] * (1 - k)
    return out


def calc_macd(closes, fast=12, slow=26, signal=9):
    ema_f = _ema(closes, fast)
    ema_s = _ema(closes, slow)
    dif = ema_f - ema_s
    dea = _ema(dif, signal)
    hist = dif - dea
    return dif, dea, hist


# ── 单股信号 ──────────────────────────────────────────────────────────────────

def _has_signal(stock):
    """MACD DIF 上穿 DEA（金叉）+ 量能放大 + 收盘在 MA20 之上"""
    data_close = history_bars(stock, 60, '1d', 'close')
    data_volume = history_bars(stock, 60, '1d', 'volume')
    if data_close is None or data_volume is None or len(data_close) < 40:
        return False

    closes = data_close.astype(float)
    volumes = data_volume.astype(float)

    dif, dea, _ = calc_macd(closes)

    # DIF 金叉 DEA：昨日 DIF < DEA，今日 DIF > DEA
    if not (dif[-2] < dea[-2] and dif[-1] > dea[-1]):
        return False

    # 价格在 MA20 之上
    ma20 = np.mean(closes[-20:])
    if closes[-1] < ma20:
        return False

    # 量能放大：今日成交量 > 20日均量 × 1.5
    avg_vol = np.mean(volumes[-21:-1])
    if avg_vol <= 0 or volumes[-1] < avg_vol * 1.5:
        return False

    return True


# ── 止损 & 超期清仓 ───────────────────────────────────────────────────────────

def _manage_positions(context, bar_dict):
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(s)
        if pos is None: continue
        if pos.quantity <= 0:
            context.buy_price.pop(s, None)
            context.hold_days.pop(s, None)
            continue

        context.hold_days[s] = context.hold_days.get(s, 0) + 1

        if s in bar_dict and bar_dict[s].is_trading:
            current = bar_dict[s].close
            buy_p = context.buy_price.get(s, pos.avg_cost)
            if buy_p > 0 and (current - buy_p) / buy_p <= -context.stop_loss:
                print(f'止损 {s}，亏损 {(current-buy_p)/buy_p:.2%}')
                order_target_value(s, 0)
                context.buy_price.pop(s, None)
                context.hold_days.pop(s, None)
                continue

        if context.hold_days.get(s, 0) >= context.max_hold_days:
            print(f'超期清仓 {s}')
            order_target_value(s, 0)
            context.buy_price.pop(s, None)
            context.hold_days.pop(s, None)


# ── 选股 ──────────────────────────────────────────────────────────────────────

def get_candidates(context, bar_dict):
    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    candidates = []
    for s in all_stocks:
        code = s.split('.')[0]
        # 排除科创板、北交所
        if code.startswith('688') or code.startswith('4') or code.startswith('8'):
            continue
        # 排除ST
        try:
            info = instruments(s)
            if info is None:
                continue
            if 'ST' in info.symbol or '*' in info.symbol:
                continue
        except Exception:
            continue
        if s not in bar_dict or not bar_dict[s].is_trading:
            continue
        try:
            if _has_signal(s):
                candidates.append(s)
        except Exception:
            continue

    # 按5日动量排序
    scored = []
    for s in candidates:
        closes = history_bars(s, 6, '1d', 'close')
        if closes is not None and len(closes) >= 6:
            mom = float(closes[-1] / closes[0] - 1)
            scored.append((s, mom))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[: context.stock_num]]


# ── 交易主函数 ────────────────────────────────────────────────────────────────

def my_trade(context, bar_dict):
    _manage_positions(context, bar_dict)

    current_positions = [s for s, p in context.portfolio.positions.items() if p.quantity > 0]
    slots = context.stock_num - len(current_positions)
    if slots <= 0:
        return

    target = get_candidates(context, bar_dict)
    to_buy = [s for s in target if s not in current_positions][:slots]
    if not to_buy:
        return

    per_value = context.portfolio.total_value * 0.95 / context.stock_num
    for s in to_buy:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, per_value)
            context.buy_price[s] = bar_dict[s].open
            context.hold_days[s] = 0
            print(f'买入 {s}')
