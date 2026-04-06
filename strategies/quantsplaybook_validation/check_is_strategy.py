"""
Check all non-SKIP files: are they real strategies or just docs/stubs?
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'
files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])

not_strategy = []
for fname in files:
    path = os.path.join(BASE, fname)
    c = open(path).read()
    if 'SKIP_REASON' in c:
        continue
    lines = c.split('\n')
    code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]

    has_order = any('order_' in l for l in code_lines)
    has_init = any('def init(' in l for l in code_lines)
    has_handle = any('def handle_bar(' in l for l in code_lines)
    has_scheduler = any('scheduler.' in l for l in code_lines)

    # Minimal stub: only pass/imports/def stubs
    real_code = [l for l in code_lines
                 if l.strip() not in ('pass', '')
                 and not l.strip().startswith('def ')
                 and not l.strip().startswith('import ')
                 and not l.strip().startswith('from ')]

    if not has_order and len(real_code) < 5:
        not_strategy.append((fname, 'no order calls, minimal code'))
    elif not has_init and not has_handle:
        not_strategy.append((fname, 'no init() or handle_bar()'))

print(f'Suspicious (not real strategy): {len(not_strategy)}')
for f, reason in not_strategy:
    print(f'  {f}: {reason}')
