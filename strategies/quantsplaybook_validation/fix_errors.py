"""
Fix all runtime error patterns found in strategy files
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'
files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
fixed = []

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    new_lines = []
    changed = False

    for line in lines:
        new = line
        s = line.lstrip()
        if s.startswith('#'):
            new_lines.append(line)
            continue

        # 1. get_trading_dates(end_date=context.now, -> context.now.date()
        if 'get_trading_dates(' in new and 'end_date=context.now,' in new:
            new = new.replace('end_date=context.now,', 'end_date=context.now.date(),')

        # 2. entry_date=context.now) -> entry_date=context.now.date()
        if 'entry_date=context.now)' in new:
            new = new.replace('entry_date=context.now)', 'entry_date=context.now.date())')

        # 3. fundamentals.stockcode.in_ -> order_book_id.in_
        if 'fundamentals.eod_derivative_indicator.stockcode.in_(' in new:
            new = new.replace(
                'fundamentals.eod_derivative_indicator.stockcode.in_(',
                'fundamentals.eod_derivative_indicator.order_book_id.in_('
            )

        # 4. bar.last -> bar.close (bar_dict access)
        if 'bar_dict[' in new and '].last' in new:
            new = new.replace('].last', '].close')
        if 'bar.last' in new and 'bar_dict' not in new:
            # standalone bar.last
            new = new.replace('bar.last', 'bar.close')

        # 5. all_instruments(type='CS') -> all_instruments('CS')
        if "all_instruments(type='CS')" in new:
            new = new.replace("all_instruments(type='CS')", "all_instruments('CS')")
        if 'all_instruments(type="CS")' in new:
            new = new.replace('all_instruments(type="CS")', "all_instruments('CS')")

        # 6. all_instruments(['LOF', 'ETF']) -> all_instruments('LOF') + all_instruments('ETF')
        # handled separately below

        # 7. s.status == 'Active' -> remove this filter (instruments don't have .status in RQ)
        if "s.status == 'Active'" in new:
            new = new.replace(" and s.status == 'Active'", '')
            new = new.replace("s.status == 'Active' and ", '')
            new = new.replace("s.status == 'Active'", 'True')

        # 8. get_previous_trading_date -> use get_trading_dates
        if 'get_previous_trading_date(' in new:
            # Replace: get_previous_trading_date(today, 60) -> get_trading_dates(end_date=today, count=61)[0]
            import re
            m = re.search(r'get_previous_trading_date\((\w+),\s*(\d+)\)', new)
            if m:
                date_var = m.group(1)
                n = int(m.group(2))
                replacement = f'get_trading_dates(end_date={date_var}, count={n+1})[0]'
                new = new[:m.start()] + replacement + new[m.end():]

        # 9. history_bars with list of stocks - can't fix automatically, skip

        if new != line:
            changed = True
        new_lines.append(new)

    if changed:
        open(path, 'w').writelines(new_lines)
        fixed.append(fname)

print(f'Fixed: {len(fixed)} files')
for f in fixed:
    print(f'  {f}')
