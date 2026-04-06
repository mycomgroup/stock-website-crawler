#!/usr/bin/env python3
"""
Pass 3: Fix remaining bugs
1. all_instruments_iter - remaining patterns not caught by pass 2
2. len(df) after get_factor (should be len(factor_df))
3. candidates_self_append remaining
4. minute_bars - replace '1m' with '1d' where it's clearly wrong
5. multiline get_factor(\\n    stocks, ...) - stocks var check
"""
import os, re

STRATEGIES_DIR = 'strategies/quantsplaybook_validation/strategies'

def fix_all_instruments_iter(code):
    """Fix: stock_ids = [s.order_book_id for s in instruments_df if not s.order_book_id.startswith(...)]"""
    # Multi-tuple startswith variant
    code = re.sub(
        r'\[s\.order_book_id for s in instruments_df if not s\.order_book_id\.startswith\(([^)]+)\)\]',
        r"[s for s in instruments_df['order_book_id'].tolist() if not s.startswith(\1)]",
        code
    )
    # Simple variant without filter
    code = re.sub(
        r'\[s\.order_book_id for s in instruments_df\b([^\]]*)\]',
        lambda m: "instruments_df['order_book_id'].tolist()" if not m.group(1).strip() else m.group(0),
        code
    )
    return code

def fix_len_df_after_get_factor(code):
    """Fix: if factor_df is None or len(df) == 0 → len(factor_df)"""
    code = re.sub(
        r'(if factor_df is None or )len\(df\)(\s*==\s*0)',
        r'\1len(factor_df)\2',
        code
    )
    # Also: if factor_df is None or factor_df.empty
    # And: if df is None or len(df) == 0 right after factor_df assignment
    return code

def fix_candidates_self_append(code):
    if not (re.search(r'candidates\.append\(', code) and re.search(r'for \w+ in candidates', code)):
        return code
    lines = code.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'(\s+)for (\w+) in candidates:', line)
        if m:
            indent = m.group(1)
            var = m.group(2)
            j = i + 1
            has_self_append = False
            while j < len(lines):
                bl = lines[j]
                if bl.strip() and not bl.startswith(indent + ' ') and not bl.startswith(indent + '\t'):
                    break
                if f'candidates.append({var}' in bl or f'candidates.append(({var}' in bl:
                    has_self_append = True
                j += 1
            if has_self_append:
                new_lines.append(indent + 'result = []')
                new_lines.append(line)
                i += 1
                while i < j:
                    bl = lines[i]
                    bl = bl.replace(f'candidates.append({var})', f'result.append({var})')
                    bl = bl.replace(f'candidates.append(({var},', f'result.append(({var},')
                    new_lines.append(bl)
                    i += 1
                continue
        new_lines.append(line)
        i += 1
    code = '\n'.join(new_lines)
    if 'result = []' in code:
        code = re.sub(r'context\.candidates = candidates\[:(.*?)\]', r'context.candidates = result[:\1]', code)
        code = re.sub(r'context\.candidates = \[s for s, _ in candidates\[:(.*?)\]\]',
                      r'context.candidates = [s for s, _ in result[:\1]]', code)
    return code

def fix_multiline_get_factor_stocks(code):
    """
    Fix multiline:
        factor_df = get_factor(
            stocks,
    where stocks is not defined in the current function scope.
    """
    # Find multiline get_factor( \n    stocks,
    pattern = re.compile(r'(factor_df\s*=\s*get_factor\(\s*\n\s+)(stocks)(\s*,)', re.MULTILINE)

    def replace_stocks(m):
        prefix = m.group(1)
        suffix = m.group(3)
        # Find what variable to use - look backwards in code
        pos = m.start()
        before = code[:pos]
        last_func = before.split('def ')[-1]
        if re.search(r'\bstocks\s*=', last_func):
            return m.group(0)  # stocks is defined, leave as-is
        for var in ['stock_ids', 'pool', 'list_stock', 'all_stocks', 'valid', 'candidates']:
            if re.search(rf'\b{var}\s*=', last_func):
                return prefix + var + suffix
        return m.group(0)

    code = pattern.sub(replace_stocks, code)
    return code

def fix_minute_bars_in_day_strategy(code):
    """
    For strategies that use scheduler.run_daily (day-frequency),
    replace history_bars(..., '1m', ...) with '1d' where it's fetching
    simple price data (not intraday logic).
    Only fix obvious cases: history_bars(stock, N, '1m', 'close'/'open'/'high'/'low')
    where N is small (1-5) and it's clearly meant to get recent daily bars.
    """
    # Only fix if it's a day-frequency strategy (has run_daily but not run_minute)
    if 'run_daily' not in code:
        return code
    # Don't touch strategies that are explicitly intraday
    if 'run_minute' in code or 'bar_dict[' in code and "'1m'" in code:
        # Be conservative - only fix history_bars with '1m' for close/open
        pass

    # Fix: history_bars(stock, 1, '1m', 'close') → history_bars(stock, 2, '1d', 'close')
    # (1 minute bar → 2 day bars to get yesterday's close)
    code = re.sub(
        r"history_bars\((\w+),\s*1,\s*'1m',\s*'close'\)",
        r"history_bars(\1, 2, '1d', 'close')",
        code
    )
    code = re.sub(
        r"history_bars\((\w+),\s*2,\s*'1m',\s*'close'\)",
        r"history_bars(\1, 3, '1d', 'close')",
        code
    )
    return code

def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        original = f.read()
    code = original
    changes = []

    if re.search(r'\[s\.order_book_id for s in instruments_df', code):
        code = fix_all_instruments_iter(code)
        changes.append('all_instruments_iter')

    if re.search(r'if factor_df is None or len\(df\)', code):
        code = fix_len_df_after_get_factor(code)
        changes.append('len_df_typo')

    if re.search(r'candidates\.append\(', code) and re.search(r'for \w+ in candidates', code):
        code = fix_candidates_self_append(code)
        changes.append('candidates_self_append')

    # Multiline get_factor stocks
    if re.search(r'get_factor\(\s*\n\s+stocks\s*,', code):
        code = fix_multiline_get_factor_stocks(code)
        changes.append('multiline_get_factor_stocks')

    if code != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return changes
    return []

def main():
    files = sorted([f for f in os.listdir(STRATEGIES_DIR) if f.endswith('.py')])
    total = 0
    for fname in files:
        path = os.path.join(STRATEGIES_DIR, fname)
        changes = fix_file(path)
        if changes:
            total += 1
            print(f'✓ {fname}: {changes}')
    print(f'\n共修复 {total} 个文件')

if __name__ == '__main__':
    main()
