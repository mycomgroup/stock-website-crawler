"""
检查策略文件中残留的 JoinQuant API 问题
只扫描非注释行，避免误报
"""
import os

base = 'strategies/quantsplaybook_validation/strategies'

# (substring_to_find, label)
# 只检查非注释行中出现的字符串
BAD_STRINGS = [
    ('get_current_data()', 'get_current_data'),
    ('log.set_level(', 'log.set_level'),
    ('logger.set_level(', 'logger.set_level'),
    ('available_cash', 'available_cash'),
    ('get_all_securities(', 'get_all_securities'),
    ('from jqdata', 'from jqdata'),
    ('position.security', 'position.security'),
    ('context.current_dt', 'context.current_dt'),
    ('context.previous_date', 'context.previous_date'),
    ('portfolio.portfolio_value', 'portfolio.portfolio_value'),
    ('schedule_function(', 'schedule_function'),
]

# 这些需要额外检查：只有在 JQ ORM 风格时才是问题
JQ_ORM_MARKERS = ['valuation.', 'indicator.', 'cash_flow.', 'income.', 'balance.']

files = sorted([f for f in os.listdir(base) if f.endswith('.py')])
needs_fix = []

for fname in files:
    path = os.path.join(base, fname)
    lines = open(path).readlines()

    # Skip SKIP files
    if any('SKIP_REASON' in l for l in lines):
        continue

    found = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('#'):
            continue  # skip comment lines

        for substr, label in BAD_STRINGS:
            if substr in line and label not in found:
                found.append(label)

        # Check get_fundamentals with JQ ORM fields
        if 'get_fundamentals(' in line:
            for marker in JQ_ORM_MARKERS:
                if marker in line and 'get_fundamentals JQ ORM' not in found:
                    found.append('get_fundamentals JQ ORM')

    if found:
        needs_fix.append((fname, found))

print(f'Still needs fix: {len(needs_fix)}')
for f, p in needs_fix:
    print(f'  {f}: {p}')
