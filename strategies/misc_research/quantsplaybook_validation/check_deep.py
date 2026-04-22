"""
Deep check: scan for genuinely broken JQ-specific patterns in non-comment lines.
No regex - pure string operations.
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

# Patterns that are definitely broken in RQ
# (substring, label, exclude_if_also_contains)
BROKEN = [
    # JQ-only functions
    ('get_current_data()', 'get_current_data', None),
    ('from jqdata', 'from jqdata', None),
    ('get_all_securities(', 'get_all_securities', None),
    ('schedule_function(', 'schedule_function', None),
    ('finance.run_query(', 'finance.run_query', None),
    ('get_extras(', 'get_extras', None),
    ('get_current_tick(', 'get_current_tick', None),
    ('get_security_info(', 'get_security_info', None),
    ('get_index_stocks(', 'get_index_stocks', None),
    ('get_industry_stocks(', 'get_industry_stocks', None),
    ('get_trade_dates(', 'get_trade_dates (use get_trading_dates)', None),
    ('unschedule_all()', 'unschedule_all', None),
    ('after_code_changed', 'after_code_changed', None),
    ('inout_cash(', 'inout_cash', None),
    ('set_universe(', 'set_universe', None),
    # JQ imports
    ('import jqlib', 'jqlib import', None),
    ('from jqlib', 'jqlib import', None),
    ('import jqfactor', 'jqfactor import', None),
    ('from jqfactor', 'jqfactor import', None),
    ('import talib', 'talib import', None),
    # Wrong attribute names
    ('context.current_dt', 'context.current_dt (use context.now)', None),
    ('context.previous_date', 'context.previous_date', None),
    ('context.current_date', 'context.current_date (use context.now.date())', None),
    ('available_cash', 'available_cash (use .cash)', None),
    ('portfolio.portfolio_value', 'portfolio_value (use .total_value)', None),
    ('position.security', 'position.security (use .order_book_id)', None),
    # log
    ('log.set_level(', 'log.set_level', None),
    ('logger.set_level(', 'logger.set_level', None),
    # record() is JQ only
    ('record(', 'record() JQ only', None),
    # bare run_daily/monthly/weekly (not preceded by scheduler.)
    # checked manually below
    # JQ ORM: valuation. or indicator. used OUTSIDE of fundamentals.xxx context
    # We check: line has 'valuation.' but NOT 'fundamentals.'
    # checked manually below
]

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
results = {}

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()

    if any('SKIP_REASON' in l for l in lines):
        continue

    found = {}

    for lineno, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith('#'):
            continue

        for substr, label, exclude in BROKEN:
            if substr not in line:
                continue
            if exclude and exclude in line:
                continue
            # Special exclusions
            if substr == 'available_cash' and 'portfolio.cash' in line:
                continue
            if substr == 'record(' and ('# record(' in line or 'order_record' in line or 'trade_record' in line):
                continue
            if substr == 'get_security_info(' and '# get_security_info' in line:
                continue
            if label not in found:
                found[label] = []
            found[label].append(lineno)

        # Check bare run_daily/monthly/weekly (not scheduler.)
        for func in ('run_daily(', 'run_monthly(', 'run_weekly('):
            if func in line and 'scheduler.' + func not in line and '# ' + func not in line:
                label = f'bare {func[:-1]} (missing scheduler.)'
                if label not in found:
                    found[label] = []
                found[label].append(lineno)

        # Check JQ ORM: valuation. or indicator. NOT inside fundamentals.xxx
        for jq_prefix in ('valuation.', 'indicator.'):
            if jq_prefix in line and 'fundamentals.' not in line:
                label = f'JQ ORM: {jq_prefix}'
                if label not in found:
                    found[label] = []
                found[label].append(lineno)

    if found:
        results[fname] = found

print(f'Files with issues: {len(results)}\n')
for fname, issues in sorted(results.items()):
    print(f'{fname}:')
    for label, lns in issues.items():
        print(f'  [{label}] lines: {lns[:5]}')
    print()
