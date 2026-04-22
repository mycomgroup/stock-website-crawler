# 行业有效量价因子与行业轮动策略 - 增强版 v1.0
# 来源：《行业有效量价因子与行业轮动策略》
# 增强机制（来自 strategy_kits/universal_mechanisms）：
#   [01] 情绪开关：涨停家数过低时空仓
#   [10] 波动率仓位：ATR 高时降低整体仓位
#   [12] 市场广度：站上 MA20 比例过低时空仓
#   [17] 移动止损：持仓从高点回撤超阈值时清仓
#
# autoresearch 探索空间（顶部参数区）：
#   WINDOW, TOP_N, EMOTION_THRESHOLD, BREADTH_MIN,
#   TRAILING_STOP_RATIO, VOL_HIGH_THRESHOLD, POSITION_RATIO

import numpy as np

# ═══════════════════════════════════════════════════════
# 参数区（autoresearch 只改这里）
# ═══════════════════════════════════════════════════════

# 核心选股参数
WINDOW = 20           # 量价动量计算窗口（可探索：15~30）
TOP_N = 3             # 持仓行业数（可探索：2~5）

# 情绪开关 [机制01]
# RiceQuant 版：用沪深300近5日涨跌幅判断情绪
# 5日跌幅超过 EMOTION_THRESHOLD * 0.1% 时空仓
# 如 EMOTION_THRESHOLD=20 → 5日跌超2%时空仓（可探索：10~50）
EMOTION_THRESHOLD = 20
EMOTION_ENABLED = True   # 是否启用情绪开关

# 市场广度过滤 [机制12]
# RiceQuant 版：用沪深300指数是否站上MA20判断广度
# 指数收盘 < MA20 * BREADTH_MIN 时空仓
# 如 BREADTH_MIN=0.97 → 跌破MA20的97%时空仓（可探索：0.93~0.99）
BREADTH_MIN = 0.97       # MA 折扣系数（可探索：0.93~0.99）
BREADTH_ENABLED = True   # 是否启用广度过滤
BREADTH_MA = 20          # 广度计算用的均线周期

# 移动止损 [机制17]
TRAILING_STOP_RATIO = 0.08   # 从持仓高点回撤超过此比例止损（可探索：0.05~0.15）
TRAILING_STOP_ENABLED = True

# 波动率仓位 [机制10]
VOL_HIGH_THRESHOLD = 0.04    # ETF日均ATR/价格超过此值时降仓（可探索：0.03~0.06）
VOL_LOW_POSITION = 0.6       # 高波动时仓位（可探索：0.4~0.7）
VOL_ENABLED = True

# 调仓频率
REBALANCE_FREQ = 'monthly'   # 'monthly' 或 'weekly'（可探索）

# ═══════════════════════════════════════════════════════
# 行业 ETF 池
# ═══════════════════════════════════════════════════════

INDUSTRY_ETFS = {
    '510880.XSHG': '红利ETF',
    '512010.XSHG': '军工ETF',
    '512660.XSHG': '军工ETF2',
    '512800.XSHG': '银行ETF',
    '515000.XSHG': '科技ETF',
    '515030.XSHG': '新能源ETF',
    '159928.XSHE': '消费ETF',
    '159915.XSHE': '创业板ETF',
    '159905.XSHE': '油气ETF',
    '159869.XSHE': '医疗ETF',
}

# ═══════════════════════════════════════════════════════
# 核心因子计算
# ═══════════════════════════════════════════════════════

def calc_pv_momentum(prices, volumes, window=20):
    """量价动量因子：价格动量 * 成交量趋势"""
    if len(prices) < window + 1:
        return None
    p = np.array(prices[-(window + 1):], dtype=float)
    v = np.array(volumes[-window:], dtype=float)

    price_mom = (p[-1] / p[0]) - 1
    vol_trend = np.corrcoef(np.arange(window), v)[0, 1] if np.std(v) > 0 else 0

    return price_mom * (1 + vol_trend)


# ═══════════════════════════════════════════════════════
# 机制01：情绪开关（RiceQuant 版）
# 用沪深300近5日涨跌幅代替涨停家数：
#   5日涨幅 < -EMOTION_THRESHOLD% 时视为情绪低迷，空仓
# ═══════════════════════════════════════════════════════

def check_emotion(context):
    """市场情绪过差时返回 False，禁止开仓"""
    if not EMOTION_ENABLED:
        return True
    try:
        # 用沪深300近5日收益率判断情绪
        closes = history_bars('000300.XSHG', 6, '1d', 'close')
        if closes is None or len(closes) < 6:
            return True
        ret_5d = (float(closes[-1]) / float(closes[0])) - 1
        # EMOTION_THRESHOLD 复用为跌幅阈值（如 20 → -0.020，即5日跌超2%空仓）
        threshold = -EMOTION_THRESHOLD * 0.001
        return ret_5d >= threshold
    except Exception:
        return True  # 获取失败时不阻断


# ═══════════════════════════════════════════════════════
# 机制12：市场广度过滤（RiceQuant 版）
# 用沪深300指数价格是否站上 MA20 来代替广度计算：
#   指数收盘 < MA20 * BREADTH_MIN 时视为广度不足，空仓
#   （BREADTH_MIN 在此语义下为 MA 折扣系数，如 0.97 表示跌破MA3%才空仓）
# ═══════════════════════════════════════════════════════

def check_breadth(context):
    """指数跌破 MA20 一定幅度时返回 False"""
    if not BREADTH_ENABLED:
        return True
    try:
        closes = history_bars('000300.XSHG', BREADTH_MA + 1, '1d', 'close')
        if closes is None or len(closes) < BREADTH_MA + 1:
            return True
        closes = np.array(closes, dtype=float)
        ma20 = np.mean(closes[-BREADTH_MA:])
        current = closes[-1]
        # BREADTH_MIN 复用为 MA 折扣系数（如 0.97 → 跌破MA的97%才空仓）
        return current >= ma20 * BREADTH_MIN
    except Exception:
        return True


# ═══════════════════════════════════════════════════════
# 机制10：波动率仓位
# ═══════════════════════════════════════════════════════

def calc_portfolio_atr_ratio(context, etfs):
    """计算持仓 ETF 的平均 ATR/价格比率"""
    if not VOL_ENABLED or not etfs:
        return 0.0
    ratios = []
    for etf in etfs:
        try:
            bars = history_bars(etf, WINDOW + 1, '1d', ['high', 'low', 'close'])
            if bars is None or len(bars) < WINDOW + 1:
                continue
            high = np.array(bars['high'], dtype=float)
            low = np.array(bars['low'], dtype=float)
            close = np.array(bars['close'], dtype=float)
            tr = np.maximum(high[1:] - low[1:],
                            np.maximum(np.abs(high[1:] - close[:-1]),
                                       np.abs(low[1:] - close[:-1])))
            atr = np.mean(tr[-WINDOW:])
            price = close[-1]
            if price > 0:
                ratios.append(atr / price)
        except Exception:
            continue
    return np.mean(ratios) if ratios else 0.0


def get_vol_position_ratio(context, etfs):
    """根据波动率返回仓位比例"""
    if not VOL_ENABLED:
        return 0.95
    atr_ratio = calc_portfolio_atr_ratio(context, etfs)
    if atr_ratio > VOL_HIGH_THRESHOLD:
        return VOL_LOW_POSITION
    return 0.95


# ═══════════════════════════════════════════════════════
# 机制17：移动止损
# ═══════════════════════════════════════════════════════

def _current_price(pos):
    """RiceQuant StockPositionProxy 用 market_value/quantity 取当前价"""
    try:
        if pos.quantity > 0:
            return pos.market_value / pos.quantity
    except Exception:
        pass
    return pos.avg_price  # fallback 到成本价


def _avg_price(pos):
    """RiceQuant 持仓成本字段是 avg_price，不是 avg_cost"""
    return pos.avg_price


def update_high_prices(context):
    """更新各持仓 ETF 的历史最高价"""
    for etf, pos in context.portfolio.positions.items():
        current_price = _current_price(pos)
        if etf not in context.high_prices:
            context.high_prices[etf] = current_price
        elif current_price > context.high_prices[etf]:
            context.high_prices[etf] = current_price


def check_trailing_stop(context):
    """检查并执行移动止损，返回被止损的 ETF 列表"""
    if not TRAILING_STOP_ENABLED:
        return []
    stopped = []
    for etf, pos in list(context.portfolio.positions.items()):
        high = context.high_prices.get(etf, _avg_price(pos))
        current = _current_price(pos)
        if high > 0 and (current - high) / high <= -TRAILING_STOP_RATIO:
            order_target_value(etf, 0)
            context.high_prices.pop(etf, None)
            stopped.append(etf)
            print(f'[止损] {etf} 从高点 {high:.3f} 回撤至 {current:.3f}，触发移动止损')
    return stopped


# ═══════════════════════════════════════════════════════
# RiceQuant 入口
# ═══════════════════════════════════════════════════════

def init(context):
    context.etfs = list(INDUSTRY_ETFS.keys())
    context.last_rebalance = -1   # 上次调仓的月/周编号
    context.high_prices = {}      # etf -> 持仓期间最高价 [机制17]


def handle_bar(context, bar_dict):
    # ── 调仓频率控制 ──────────────────────────────────
    now = context.now
    if REBALANCE_FREQ == 'monthly':
        period_id = now.month
    else:  # weekly
        period_id = now.isocalendar()[1]  # ISO 周数

    if period_id == context.last_rebalance:
        # 非调仓日只做移动止损检查
        if TRAILING_STOP_ENABLED:
            update_high_prices(context)
            check_trailing_stop(context)
        return

    # ── 门控：情绪 + 广度 ─────────────────────────────
    if not check_emotion(context):
        print('[情绪开关] 指数5日跌幅过大，全部空仓')
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        context.high_prices.clear()
        context.last_rebalance = period_id
        return

    if not check_breadth(context):
        print('[广度过滤] 指数跌破MA20，全部空仓')
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        context.high_prices.clear()
        context.last_rebalance = period_id
        return

    # ── 计算量价动量因子 ──────────────────────────────
    scores = {}
    for etf in context.etfs:
        try:
            prices = history_bars(etf, WINDOW + 2, '1d', 'close')
            volumes = history_bars(etf, WINDOW + 1, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            factor = calc_pv_momentum(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                WINDOW
            )
            if factor is not None:
                scores[etf] = factor
        except Exception:
            continue

    if not scores:
        context.last_rebalance = period_id
        return

    # ── 选出 TopN ─────────────────────────────────────
    sorted_etfs = sorted(scores, key=scores.get, reverse=True)
    target = sorted_etfs[:TOP_N]

    # ── 波动率仓位 ────────────────────────────────────
    position_ratio = get_vol_position_ratio(context, target)

    # ── 执行调仓 ──────────────────────────────────────
    # 先清掉不在目标里的持仓
    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)
            context.high_prices.pop(etf, None)

    # 买入目标 ETF
    weight = position_ratio / len(target)
    total_value = context.portfolio.total_value
    for etf in target:
        order_target_value(etf, total_value * weight)
        # 新建仓时用 bar_dict 初始化最高价记录
        if etf not in context.high_prices:
            try:
                context.high_prices[etf] = bar_dict[etf].close
            except Exception:
                context.high_prices[etf] = 0

    context.last_rebalance = period_id
    print(f'[调仓] target={[INDUSTRY_ETFS.get(e, e) for e in target]} '
          f'position_ratio={position_ratio:.2f} scores={[round(scores[e], 4) for e in target]}')
