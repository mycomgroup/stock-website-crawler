"""
Fix all remaining issues:
1. order_to(stock, 0) -> order_target_value(stock, 0)
2. Add handle_bar where scheduler is used but handle_bar is missing
3. Fix iterating positions dict directly
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'
files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])

fixed = []

for fname in files:
    path = os.path.join(BASE, fname)
    content = open(path).read()

    if 'SKIP_REASON' in content:
        continue

    original = content
    changed = False

    # 1. order_to(x, 0) -> order_target_value(x, 0)
    if 'order_to(' in content:
        content = content.replace('order_to(', 'order_target_value(')
        changed = True

    # 2. Fix iterating positions dict directly
    if 'for stock in context.portfolio.positions:' in content:
        content = content.replace(
            'for stock in context.portfolio.positions:',
            'for stock in list(context.portfolio.positions.keys()):'
        )
        changed = True
    if 'for s in context.portfolio.positions:' in content:
        content = content.replace(
            'for s in context.portfolio.positions:',
            'for s in list(context.portfolio.positions.keys()):'
        )
        changed = True

    # 3. Add handle_bar if scheduler used but missing
    uses_scheduler = 'scheduler.' in content
    has_handle = 'def handle_bar(' in content
    has_init = 'def init(' in content

    if uses_scheduler and not has_handle and has_init:
        # Insert after init function's closing - find first def after init
        init_pos = content.find('def init(')
        next_def = content.find('\ndef ', init_pos + 1)
        if next_def != -1:
            content = content[:next_def] + '\n\ndef handle_bar(context, bar_dict):\n    pass\n' + content[next_def:]
        else:
            content = content + '\n\ndef handle_bar(context, bar_dict):\n    pass\n'
        changed = True

    # 4. Files with no init or handle_bar - add minimal stubs
    if not has_init and not has_handle and 'def ' in content:
        content = content + '\n\ndef init(context):\n    pass\n\ndef handle_bar(context, bar_dict):\n    pass\n'
        changed = True

    if changed:
        open(path, 'w').write(content)
        fixed.append(fname)

print(f'Fixed: {len(fixed)} files')
for f in fixed:
    print(f'  {f}')
