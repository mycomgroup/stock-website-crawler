"""
Deep scan for all possible runtime issues in RiceQuant strategies.
Checks every non-comment line for known bad patterns.
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

# (pattern_substring, label, exclude_if_contains)
CHECKS = [
    # Wrong time API
    ('context.current_dt', 'context.current_dt -> context.now', []),
    ('context.previous_date', 'context.previous_date (no RQ equiv)', []),
    ('context.current_date', 'context.current_date -> context.now.date()', []),

    # Wrong data API
    ('get_current_data()', 'get_current_data() JQ only', []),
    ('attribute_history(', 'attribute_history JQ only', []),
    ('get_all_securities(', 'get_all_securities JQ only', []),
    ('get_index_stocks(', 'get_index_stocks -> index_components', []),
    ('get_trade_dates(', 'get_trade_dates -> get_trading_dates', ['get_trading_dates']),
    ('get_previous_trading_date(', 'get_previous_trading_date not in RQ', []),
    ('get_extras(', 'get_extras JQ only', []),
    ('get_current_tick(', 'get_current_tick JQ only', []),
    ('get_security_info(', 'get_security_info -> instruments()', ['instruments(']),
    ('finance.run_query(', 'finance.run_query JQ only', ['# ']),
    ('finance.STK_', 'finance.STK_ JQ only', ['# ']),
    ('get_price(', 'get_price JQ only', ['# ']),
    ('from jqdata', 'from jqdata', []),
    ('import jqlib', 'jqlib', []),
    ('import jqfactor', 'jqfactor', []),
    ('import talib', 'talib', []),

    # Wrong bar/position attributes
    ('.symbol', 'bar_dict[x].symbol -> instruments(x).symbol', ['instruments(']),
    ('bar_dict[', 'bar_dict check', []),  # handled specially below
    ('position.security', 'position.security -> order_book_id', ['order_book_id']),
    ('position.price', 'position.price -> last_price', ['last_price', 'avg_cost', 'limit']),
    ('position.value', 'position.value -> market_value', ['market_value', 'total_value']),
    ('total_amount', 'total_amount -> quantity', ['quantity']),
    ('closeable_amount', 'closeable_amount -> sellable_quantity', []),
    ('available_cash', 'available_cash -> cash', ['portfolio.cash']),
    ('portfolio_value', 'portfolio_value -> total_value', ['total_value']),

    # Wrong order functions
    ('order_to(', 'order_to -> order_target_value', []),
    ('order_target(', 'order_target -> order_target_value/quantity',
     ['order_target_value(', 'order_target_quantity(', 'order_target_percent(']),

    # Wrong scheduler
    ('schedule_function(', 'schedule_function JQ only', []),
    ('run_daily(', 'bare run_daily', ['scheduler.run_daily(']),
    ('run_monthly(', 'bare run_monthly', ['scheduler.run_monthly(']),
    ('run_weekly(', 'bare run_weekly', ['scheduler.run_weekly(']),
    ('unschedule_all(', 'unschedule_all JQ only', ['# ']),
    ('after_code_changed', 'after_code_changed JQ only', ['# ']),

    # Wrong log
    ('log.info(', 'log.info -> logger.info', ['logger.info(']),
    ('log.set_level(', 'log.set_level', ['# ']),
    ('logger.set_level(', 'logger.set_level', ['# ']),

    # Wrong fundamentals filter
    ('fundamentals.eod_derivative_indicator.stockcode', 'stockcode -> order_book_id', []),
    ('entry_date=context.now)', 'entry_date=context.now missing .date()', []),

    # Wrong all_instruments syntax
    ("all_instruments(type=", "all_instruments(type= wrong syntax", []),
    ("all_instruments([", "all_instruments with list", []),

    # Wrong history_bars usage
    ('.last\n', 'bar.last -> bar.close', []),
    ('bar_dict[s].last', 'bar.last -> bar.close', []),
    ('bar_dict[stock].last', 'bar.last -> bar.close', []),
    ('.is_st', 'bar_dict.is_st not available', ['instruments(', 'special_type']),
    ('.paused', 'bar_dict.paused -> is_trading', ['is_trading', 'instruments(']),

    # Wrong record
    ('record(', 'record() JQ only', ['# record(', 'order_record', 'trade_record', 'records', 'record_id']),

    # Wrong portfolio
    ('context.portfolio.positions_value', 'positions_value -> market_value', []),
    ('context.portfolio.long_positions', 'long_positions futures only', []),
    ('context.portfolio.short_positions', 'short_positions futures only', []),

    # Wrong instruments
    ('s.status ==', 'instruments.status not available', []),
    ("s.status == 'Active'", 'instruments.status not available', []),
]

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
results = {}

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    content = ''.join(lines)
    fi = []

    for lineno, line in enumerate(lines, 1):
        s = line.lstrip()
        if s.startswith('#'):
            continue

        for substr, label, excludes in CHECKS:
            if substr not in line:
                continue
            skip = any(exc in line for exc in excludes)
            if skip:
                continue

            # Special: bar_dict check - only flag .symbol and .last
            if substr == 'bar_dict[':
                if '.symbol' in line and 'instruments(' not in line:
                    fi.append((lineno, 'bar_dict[x].symbol -> instruments(x).symbol', line.rstrip()[:80]))
                if '].last' in line:
                    fi.append((lineno, 'bar.last -> bar.close', line.rstrip()[:80]))
                continue

            fi.append((lineno, label, line.rstrip()[:80]))

    if fi:
        # Deduplicate by label
        seen = {}
        for lineno, label, line in fi:
            if label not in seen:
                seen[label] = (lineno, line)
        results[fname] = seen

print(f'Files with issues: {len(results)}\n')
total = 0
for fname, issues in sorted(results.items()):
    print(f'{fname}:')
    for label, (lineno, line) in sorted(issues.items()):
        total += 1
        print(f'  L{lineno} [{label}]')
        print(f'    {line}')
    print()

print(f'Total unique issue types across files: {total}')
