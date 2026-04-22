"""
Runtime issue checker - no regex, fast string ops only
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
issues = []

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    content = ''.join(lines)

    if 'SKIP_REASON' in content:
        continue

    fi = []

    has_init = any('def init(' in l for l in lines)
    has_handle = any('def handle_bar(' in l for l in lines)

    if not has_init and not has_handle:
        fi.append('no init() or handle_bar()')

    uses_scheduler = any('scheduler.' in l and not l.lstrip().startswith('#') for l in lines)
    if uses_scheduler and not has_handle:
        fi.append('scheduler used but no handle_bar()')

    for l in lines:
        if l.lstrip().startswith('#'):
            continue
        if 'order_to(' in l:
            fi.append('order_to() - use order_target_value()')
            break

    for l in lines:
        if l.lstrip().startswith('#'):
            continue
        if 'for stock in context.portfolio.positions:' in l:
            fi.append('iterating positions dict directly - use .keys()')
            break
        if 'for s in context.portfolio.positions:' in l:
            fi.append('iterating positions dict directly - use .keys()')
            break

    if fi:
        issues.append((fname, fi))

print(f'Files with issues: {len(issues)}')
for f, iss in issues:
    print(f'  {f}:')
    for i in iss:
        print(f'    - {i}')
