"""
全面检查所有曾经修复过的错误类型，看是否还有遗漏
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

# 每个检查项: (描述, 触发条件函数)
# 触发条件: line -> True 表示有问题
CHECKS = [
    # ── 函数名 ──────────────────────────────────────────────────────────────
    ('def initialize(',         'initialize -> init'),
    ('from jqdata',             'from jqdata import'),

    # ── 全局变量 ─────────────────────────────────────────────────────────────
    # g. 后跟小写字母（排除 g.ETF 等大写开头的误报）
    # 用简单字符串检查
    ('g.stock',                 'g.stock -> context.stock'),
    ('g.buy',                   'g.buy -> context.buy'),
    ('g.hold',                  'g.hold -> context.hold'),
    ('g.ref_stock',             'g.ref_stock -> context.ref_stock'),
    ('g.slope',                 'g.slope -> context.slope'),
    ('g.etf',                   'g.etf -> context.etf'),
    ('g.num',                   'g.num -> context.num'),
    ('g.timing',                'g.timing -> context.timing'),

    # ── 定时任务 ─────────────────────────────────────────────────────────────
    ('schedule_function(',      'schedule_function (JQ only)'),
    ('run_daily(',              'bare run_daily (missing scheduler.)'),
    ('run_monthly(',            'bare run_monthly (missing scheduler.)'),
    ('run_weekly(',             'bare run_weekly (missing scheduler.)'),

    # ── 数据 API ─────────────────────────────────────────────────────────────
    ('get_current_data()',      'get_current_data()'),
    ('attribute_history(',      'attribute_history (JQ only)'),
    ('get_all_securities(',     'get_all_securities'),
    ('get_index_stocks(',       'get_index_stocks -> index_components'),
    ('get_trade_dates(',        'get_trade_dates -> get_trading_dates'),
    ('get_extras(',             'get_extras (JQ only)'),
    ('get_current_tick(',       'get_current_tick (JQ only)'),
    ('get_security_info(',      'get_security_info (JQ only)'),
    ('finance.run_query(',      'finance.run_query (JQ only)'),
    ('finance.STK_',            'finance.STK_ (JQ only)'),
    ('finance.FUND_',           'finance.FUND_ (JQ only)'),

    # ── 交易函数 ─────────────────────────────────────────────────────────────
    ('order_to(',               'order_to -> order_target_value'),
    ('order_target(',           'order_target -> order_target_value/quantity'),

    # ── 持仓属性 ─────────────────────────────────────────────────────────────
    ('position.security',       'position.security -> order_book_id'),
    ('position.price',          'position.price -> last_price'),
    ('.total_amount',           'total_amount -> quantity'),
    ('closeable_amount',        'closeable_amount -> sellable_quantity'),
    ('available_cash',          'available_cash -> cash'),
    ('portfolio_value',         'portfolio_value -> total_value'),

    # ── 时间 ─────────────────────────────────────────────────────────────────
    ('context.current_dt',      'context.current_dt -> context.now'),
    ('context.previous_date',   'context.previous_date'),
    ('context.current_date',    'context.current_date -> context.now.date()'),

    # ── 日志 ─────────────────────────────────────────────────────────────────
    ('log.info(',               'log.info -> logger.info'),
    ('log.warn(',               'log.warn -> logger.warn'),
    ('log.error(',              'log.error -> logger.error'),
    ('log.set_level(',          'log.set_level'),
    ('logger.set_level(',       'logger.set_level'),

    # ── 其他 JQ 专有 ─────────────────────────────────────────────────────────
    ('unschedule_all(',         'unschedule_all (JQ only)'),
    ('after_code_changed',      'after_code_changed (JQ only)'),
    ('process_initialize',      'process_initialize (JQ only)'),
    ('record(',                 'record() (JQ only)'),
    ('inout_cash(',             'inout_cash (JQ only)'),
    ('set_universe(',           'set_universe (JQ only)'),
    ('get_industry_stocks(',    'get_industry_stocks (JQ only)'),
    ('import jqlib',            'jqlib import'),
    ('from jqlib',              'jqlib import'),
    ('import jqfactor',         'jqfactor import'),
    ('from jqfactor',           'jqfactor import'),
    ('import talib',            'talib import'),

    # ── history_bars 用法 ────────────────────────────────────────────────────
    ('.low[',                   'data.low[] -> data["low"][]'),
    ('.high[',                  'data.high[] -> data["high"][]'),
    ('.close[',                 'data.close[] -> data["close"][]'),

    # ── bar_dict 误用 ────────────────────────────────────────────────────────
    ('.is_st',                  'bar_dict.is_st not available'),
    ('.paused',                 '.paused -> .is_trading'),
]

# 排除规则: (substr, exclude_if_line_contains)
EXCLUDES = {
    'run_daily(':           ['scheduler.run_daily('],
    'run_monthly(':         ['scheduler.run_monthly('],
    'run_weekly(':          ['scheduler.run_weekly('],
    'available_cash':       ['portfolio.cash', '# '],
    'position.security':    ['order_book_id'],
    'position.price':       ['last_price', 'avg_cost', 'close_price', 'limit'],
    '.total_amount':        ['quantity'],
    'record(':              ['# record(', 'order_record', 'trade_record', 'record_id', 'records'],
    '.is_st':               ['instruments(', 'special_type'],
    '.paused':              ['is_trading', 'instruments('],
    '.low[':                ['fundamentals', 'data[', '"low"', "'low'"],
    '.high[':               ['fundamentals', 'data[', '"high"', "'high'"],
    '.close[':              ['fundamentals', 'data[', '"close"', "'close'"],
    'order_target(':        ['order_target_value(', 'order_target_quantity(', 'order_target_percent('],
    'log.info(':            ['logger.info(', '# log'],
    'log.warn(':            ['logger.warn(', '# log'],
    'log.error(':           ['logger.error(', '# log'],
    'log.set_level(':       ['# log.set_level'],
    'logger.set_level(':    ['# logger.set_level'],
    'get_security_info(':   ['# get_security_info', 'instruments('],
    'portfolio_value':      ['total_value', '# '],
    'g.stock':              ['context.', '# '],
    'g.buy':                ['context.', '# '],
    'g.hold':               ['context.', '# '],
    'g.ref_stock':          ['context.', '# '],
    'g.slope':              ['context.', '# '],
    'g.etf':                ['context.', '# '],
    'g.num':                ['context.', '# '],
    'g.timing':             ['context.', '# '],
    'after_code_changed':   ['# after_code_changed'],
    'unschedule_all(':      ['# unschedule_all'],
    'inout_cash(':          ['# inout_cash'],
}

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
results = {}

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    content = ''.join(lines)

    if 'SKIP_REASON' in content:
        continue

    found = {}
    for lineno, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith('#'):
            continue

        for substr, label in CHECKS:
            if substr not in line:
                continue

            # Apply exclusions
            excludes = EXCLUDES.get(substr, [])
            skip = False
            for exc in excludes:
                if exc in line:
                    skip = True
                    break
            if skip:
                continue

            if label not in found:
                found[label] = []
            found[label].append((lineno, line.rstrip()[:90]))

    if found:
        results[fname] = found

print(f'Files with issues: {len(results)}\n')
total_issues = 0
for fname, issues in sorted(results.items()):
    print(f'{fname}:')
    for label, hits in sorted(issues.items()):
        total_issues += len(hits)
        for lineno, line in hits[:2]:
            print(f'  [{label}] L{lineno}: {line}')
        if len(hits) > 2:
            print(f'  [{label}] ... +{len(hits)-2} more occurrences')
    print()

print(f'Total issue instances: {total_issues}')
