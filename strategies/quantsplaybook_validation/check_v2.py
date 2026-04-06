"""
全面检查 v2 - 覆盖所有历史修复过的错误类型
包括之前漏掉的模式
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
results = {}

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    content = ''.join(lines)

    if 'SKIP_REASON' in content:
        continue

    fi = []

    for lineno, line in enumerate(lines, 1):
        s = line.lstrip()
        if s.startswith('#'):
            continue

        # ── 1. 函数名 ──────────────────────────────────────────────────────
        if 'def initialize(' in line:
            fi.append((lineno, 'initialize -> init', line.rstrip()))

        # ── 2. 全局变量 g. ─────────────────────────────────────────────────
        # 检查 g. 后跟小写字母，且 g 前面是非字母（避免 linalg. 等误报）
        idx = 0
        while True:
            idx = line.find('g.', idx)
            if idx == -1:
                break
            before = line[idx-1:idx] if idx > 0 else ' '
            after = line[idx+2:idx+3]
            # g 前面必须是非字母（空格、(、=、,、[ 等），才是真正的 g.xxx
            if after.islower() and not before.isalpha():
                fi.append((lineno, 'g.xxx -> context.xxx', line.rstrip()))
                break
            idx += 2

        # ── 3. 定时任务 ────────────────────────────────────────────────────
        if 'run_daily(' in line and 'scheduler.run_daily(' not in line:
            fi.append((lineno, 'bare run_daily -> scheduler.run_daily', line.rstrip()))
        if 'run_monthly(' in line and 'scheduler.run_monthly(' not in line:
            fi.append((lineno, 'bare run_monthly -> scheduler.run_monthly', line.rstrip()))
        if 'run_weekly(' in line and 'scheduler.run_weekly(' not in line:
            fi.append((lineno, 'bare run_weekly -> scheduler.run_weekly', line.rstrip()))
        if 'schedule_function(' in line:
            fi.append((lineno, 'schedule_function (JQ only)', line.rstrip()))

        # ── 4. 数据 API ────────────────────────────────────────────────────
        if 'get_current_data()' in line:
            fi.append((lineno, 'get_current_data()', line.rstrip()))
        if 'attribute_history(' in line:
            fi.append((lineno, 'attribute_history -> history_bars', line.rstrip()))
        if 'get_all_securities(' in line:
            fi.append((lineno, 'get_all_securities -> all_instruments', line.rstrip()))
        if 'get_index_stocks(' in line:
            fi.append((lineno, 'get_index_stocks -> index_components', line.rstrip()))
        if 'get_trade_dates(' in line:
            fi.append((lineno, 'get_trade_dates -> get_trading_dates', line.rstrip()))
        if 'get_extras(' in line:
            fi.append((lineno, 'get_extras (JQ only)', line.rstrip()))
        if 'get_current_tick(' in line:
            fi.append((lineno, 'get_current_tick (JQ only)', line.rstrip()))
        if 'get_security_info(' in line and '# ' not in line[:line.find('get_security_info(')]:
            fi.append((lineno, 'get_security_info -> instruments', line.rstrip()))
        if 'finance.run_query(' in line and '# ' not in line[:line.find('finance.run_query(')]:
            fi.append((lineno, 'finance.run_query (JQ only)', line.rstrip()))
        if 'get_industry_stocks(' in line:
            fi.append((lineno, 'get_industry_stocks (JQ only)', line.rstrip()))
        if 'from jqdata' in line:
            fi.append((lineno, 'from jqdata', line.rstrip()))
        if 'import jqlib' in line or 'from jqlib' in line:
            fi.append((lineno, 'jqlib import', line.rstrip()))
        if 'import jqfactor' in line or 'from jqfactor' in line:
            fi.append((lineno, 'jqfactor import', line.rstrip()))
        if 'import talib' in line:
            fi.append((lineno, 'talib import', line.rstrip()))

        # ── 5. 交易函数 ────────────────────────────────────────────────────
        if 'order_to(' in line:
            fi.append((lineno, 'order_to -> order_target_value', line.rstrip()))
        # order_target( but NOT order_target_value/quantity/percent
        if 'order_target(' in line:
            if 'order_target_value(' not in line and 'order_target_quantity(' not in line and 'order_target_percent(' not in line:
                fi.append((lineno, 'order_target -> order_target_value/quantity', line.rstrip()))
        # order_shares(x, 0) - wrong clear
        if 'order_shares(' in line:
            after = line[line.find('order_shares(')+13:]
            parts = after.split(',')
            if len(parts) >= 2:
                arg2 = parts[1].strip().rstrip(')').strip()
                if arg2 == '0':
                    fi.append((lineno, 'order_shares(x,0) -> order_target_value(x,0)', line.rstrip()))

        # ── 6. 持仓属性 ────────────────────────────────────────────────────
        if 'position.security' in line and 'order_book_id' not in line:
            fi.append((lineno, 'position.security -> order_book_id', line.rstrip()))
        if '.total_amount' in line and '.quantity' not in line:
            fi.append((lineno, 'total_amount -> quantity', line.rstrip()))
        if 'closeable_amount' in line:
            fi.append((lineno, 'closeable_amount -> sellable_quantity', line.rstrip()))
        if 'available_cash' in line and 'portfolio.cash' not in line:
            fi.append((lineno, 'available_cash -> cash', line.rstrip()))
        if 'portfolio.portfolio_value' in line:
            fi.append((lineno, 'portfolio_value -> total_value', line.rstrip()))
        if 'position.price' in line and 'last_price' not in line and 'avg_cost' not in line and 'close_price' not in line:
            fi.append((lineno, 'position.price -> last_price', line.rstrip()))
        if 'position.value' in line and 'market_value' not in line and 'total_value' not in line:
            fi.append((lineno, 'position.value -> market_value', line.rstrip()))

        # ── 7. 时间 ────────────────────────────────────────────────────────
        if 'context.current_dt' in line:
            fi.append((lineno, 'context.current_dt -> context.now', line.rstrip()))
        if 'context.previous_date' in line:
            fi.append((lineno, 'context.previous_date', line.rstrip()))
        if 'context.current_date' in line:
            fi.append((lineno, 'context.current_date -> context.now.date()', line.rstrip()))

        # ── 8. 日志 ────────────────────────────────────────────────────────
        if 'log.info(' in line and 'logger.info(' not in line:
            fi.append((lineno, 'log.info -> logger.info', line.rstrip()))
        if 'log.set_level(' in line and '# ' not in line[:line.find('log.set_level(')]:
            fi.append((lineno, 'log.set_level', line.rstrip()))
        if 'logger.set_level(' in line and '# ' not in line[:line.find('logger.set_level(')]:
            fi.append((lineno, 'logger.set_level', line.rstrip()))

        # ── 9. history_bars 字段访问 ───────────────────────────────────────
        # data.low[  data.high[  data.close[  (should be data['low'][)
        for field in ('data.low[', 'data.high[', 'data.close[',
                      'high_low_data.low', 'high_low_data.high',
                      'bars.low', 'bars.high', 'bars.close'):
            if field in line and 'fundamentals' not in line and '"' not in line[line.find(field):line.find(field)+20]:
                fi.append((lineno, f'{field} -> use ["field"] syntax', line.rstrip()))
                break

        # ── 10. bar_dict 误用 ──────────────────────────────────────────────
        if '.is_st' in line and 'bar_dict' in line and 'instruments(' not in line:
            fi.append((lineno, 'bar_dict.is_st not available', line.rstrip()))
        if '.paused' in line and 'bar_dict' in line and 'is_trading' not in line:
            fi.append((lineno, 'bar_dict.paused -> bar_dict.is_trading', line.rstrip()))

        # ── 11. 其他 JQ 专有 ───────────────────────────────────────────────
        if 'unschedule_all(' in line and '# ' not in line[:line.find('unschedule_all(')]:
            fi.append((lineno, 'unschedule_all (JQ only)', line.rstrip()))
        if 'after_code_changed' in line and 'def after_code_changed' in line:
            fi.append((lineno, 'after_code_changed (JQ only)', line.rstrip()))
        if 'record(' in line and '# record(' not in line and 'order_record' not in line and 'trade_record' not in line and 'records' not in line and 'record_id' not in line:
            fi.append((lineno, 'record() (JQ only)', line.rstrip()))
        if 'inout_cash(' in line and '# ' not in line[:line.find('inout_cash(')]:
            fi.append((lineno, 'inout_cash (JQ only)', line.rstrip()))

        # ── 12. 函数签名缺 bar_dict ───────────────────────────────────────
        # scheduled functions must accept bar_dict
        # (checked at file level below)

    # ── 文件级检查 ─────────────────────────────────────────────────────────
    # scheduler used but no handle_bar
    uses_scheduler = any('scheduler.' in l and not l.lstrip().startswith('#') for l in lines)
    has_handle = any('def handle_bar(' in l for l in lines)
    has_init = any('def init(' in l for l in lines)
    if uses_scheduler and not has_handle:
        fi.append((0, 'scheduler used but no handle_bar()', ''))
    if not has_init and not has_handle:
        fi.append((0, 'no init() or handle_bar()', ''))

    if fi:
        results[fname] = fi

# ── 已知误报过滤 ───────────────────────────────────────────────────────────
FALSE_POSITIVES = {
    'rq_58_Debug_多标的版ETF策略.py': {'portfolio_value -> total_value'},
    'rq_62_北向资金交易能力一定强吗.py': {'finance.run_query (JQ only)'},
}

filtered = {}
for fname, issues in results.items():
    fp = FALSE_POSITIVES.get(fname, set())
    clean = [(l, label, line) for l, label, line in issues if label not in fp]
    if clean:
        filtered[fname] = clean

print(f'Files with real issues: {len(filtered)}\n')
total = 0
for fname, issues in sorted(filtered.items()):
    print(f'{fname}:')
    seen = set()
    for lineno, label, line in issues:
        key = f'{label}|{lineno}'
        if key in seen:
            continue
        seen.add(key)
        total += 1
        loc = f'L{lineno}: ' if lineno else ''
        print(f'  [{label}] {loc}{line[:80]}')
    print()

print(f'Total: {total} issues')
