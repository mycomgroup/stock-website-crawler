#!/usr/bin/env python3
import os, re

strategies_dir = 'strategies/quantsplaybook_validation/strategies'
files = sorted([f for f in os.listdir(strategies_dir) if f.endswith('.py')])
print(f'Total .py files: {len(files)}')

bugs_found = {}
for fname in files:
    path = os.path.join(strategies_dir, fname)
    with open(path) as f:
        code = f.read()
    issues = []

    # Bug 1: weekday lock
    if re.search(r'(?<!iso)weekday\(\)\s*!=\s*[0-4]', code):
        issues.append('weekday_lock')

    # Bug 2: candidates self-append (same loop var appended back to candidates)
    for m in re.finditer(r'(^[ \t]*)for\s+(\w+)\s+in\s+candidates\s*:\s*\n((?:\1[ \t]+.*\n?)*)', code, re.M):
        loop_var = m.group(2)
        block = m.group(3)
        if re.search(rf'\bcandidates\.append\(\s*\(?\s*{re.escape(loop_var)}\b', block):
            issues.append('candidates_self_append')
            break

    # Bug 3: factor_len typo
    if 'factor_len(' in code:
        issues.append('factor_len_typo')

    # Bug 4: get_factor with undefined stocks var (function-local, before call)
    for m in re.finditer(r'get_factor\(\s*stocks\s*,', code, re.S):
        before = code[:m.start()]
        func_markers = list(re.finditer(r'^def\s+\w+\s*\([^\n]*\):', before, re.M))
        func_start = func_markers[-1].start() if func_markers else 0
        func_text_before_call = before[func_start:]
        if not re.search(r'\bstocks\s*=', func_text_before_call):
            issues.append('undefined_stocks')
            break

    # Bug 5: peg factor name
    if re.search(r"'peg'", code) and 'peg_ratio' not in code:
        issues.append('peg_factor_name')

    # Bug 6: all_instruments iterated as objects
    if ('for s in instruments_df' in code or 'for s in all_instruments' in code) and '.order_book_id' in code:
        issues.append('all_instruments_iter')

    # Bug 7: len(data) but data never defined (data_close/data_high used instead)
    if re.search(r'len\(data\)', code) and re.search(r'data_close|data_high|data_low', code) and not re.search(r'\bdata\s*=', code):
        issues.append('undefined_data_var')

    # Bug 8: minute bars in day-frequency backtest
    if re.search(r"history_bars\([^)]+,\s*['\"]1m['\"]", code):
        issues.append('minute_bars')

    # Bug 9: JQ-style get_fundamentals
    if (
        'get_fundamentals(query(' in code or
        re.search(r'\b(valuation|indicator|balance|income|cash_flow)\.', code)
    ):
        issues.append('jq_fundamentals_syntax')

    # Bug 10: DataFrame.append (deprecated in pandas >= 2.0)
    if re.search(r'\.(append|join)\(all_instruments', code):
        issues.append('df_append_deprecated')

    if issues:
        bugs_found[fname] = issues

print(f'\nFiles with bugs: {len(bugs_found)}\n')
for f, issues in sorted(bugs_found.items()):
    print(f'  {f}')
    for i in issues:
        print(f'    - {i}')
