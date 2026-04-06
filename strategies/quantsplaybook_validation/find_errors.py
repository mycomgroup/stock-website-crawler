"""
Scan all strategy files for common runtime error patterns
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

# Patterns that cause runtime errors
ERROR_PATTERNS = [
    ('get_previous_trading_date(', 'get_previous_trading_date not in RQ'),
    ('entry_date=context.now)', 'entry_date=context.now should be .date()'),
    ('entry_date=context.now.strftime', 'entry_date strftime format issue'),
    ('fundamentals.company_code', 'fundamentals.company_code wrong field'),
    ('fundamentals.stockcode', 'fundamentals.stockcode wrong field'),
    ('bar.last', 'bar.last should be bar.close'),
    ('all_instruments(type=', 'all_instruments(type= wrong syntax'),
    ('all_instruments([', 'all_instruments with list arg'),
    ('get_price(', 'get_price JQ only'),
    ('history_bars(stocks,', 'history_bars with list'),
    ('history_bars(lofs', 'history_bars with list'),
    ('history_bars(stock_list', 'history_bars with list'),
    ('history_bars(hold_list', 'history_bars with list'),
    ('history_bars(etf_list', 'history_bars with list'),
    ('.set_index(\'order_book_id\')', 'set_index order_book_id after get_fundamentals'),
    ('df.columns = [c.split', 'df.columns rename - may fail if columns differ'),
    ('context.now.strftime', 'context.now.strftime ok but check format'),
    ('position.last_price', 'position.last_price - check if valid'),
    ('bar_dict[stock].last', 'bar.last should be bar.close'),
    ('bar_dict[s].last', 'bar.last should be bar.close'),
    ('.last\n', 'bar.last should be bar.close'),
    ('order_book_id.in_(', 'order_book_id.in_ - check fundamentals filter syntax'),
    ('fundamentals.eod_derivative_indicator.stockcode', 'stockcode wrong - use order_book_id'),
    ('get_trading_dates(end_date=context.now,', 'get_trading_dates end_date=context.now (missing .date())'),
    ('get_previous_trading_date', 'get_previous_trading_date not RQ API'),
    ('context.portfolio.positions_value', 'positions_value -> market_value'),
    ('context.portfolio.long_positions', 'long_positions - futures only'),
    ('context.portfolio.short_positions', 'short_positions - futures only'),
    ('order(context.code', 'order() - futures style'),
    ('order(pos.security', 'order() with security - wrong'),
    ('instruments(stock).status', 'instruments.status field check'),
    ('s.status ==', 'instruments.status check'),
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
        for pat, label in ERROR_PATTERNS:
            if pat in line:
                fi.append((lineno, label, line.rstrip()[:80]))
    if fi:
        results[fname] = fi

print(f'Files with potential errors: {len(results)}\n')
for fname, issues in sorted(results.items()):
    print(f'{fname}:')
    seen = set()
    for lineno, label, line in issues:
        if label not in seen:
            seen.add(label)
            print(f'  L{lineno} [{label}]')
            print(f'    {line}')
    print()
