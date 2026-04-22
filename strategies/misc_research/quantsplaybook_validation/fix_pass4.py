#!/usr/bin/env python3
"""
Pass 4: Fix all remaining bugs with precise patterns
"""
import os, re

STRATEGIES_DIR = 'strategies/quantsplaybook_validation/strategies'

def fix_all_instruments_iter(code):
    """
    Fix ALL variants of:
      stock_ids = [s.order_book_id for s in instruments_df if not s.order_book_id.startswith(X)]
    →
      stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(X)]
    """
    # Match any tuple/string in startswith(...)
    code = re.sub(
        r'\[s\.order_book_id\s+for s in instruments_df\s+if not s\.order_book_id\.startswith\(([^)]+)\)\]',
        r"[s for s in instruments_df['order_book_id'].tolist() if not s.startswith(\1)]",
        code
    )
    # Also handle without filter
    code = re.sub(
        r'\[s\.order_book_id\s+for s in instruments_df\]',
        r"instruments_df['order_book_id'].tolist()",
        code
    )
    # Remove dead stock_ids lines that are now redundant (followed by stocks = [s for s in stock_ids...])
    # Leave them - they're harmless
    return code

def fix_candidates_self_append(code):
    """Fix for any loop variable name, not just 'stock'"""
    if not re.search(r'candidates\.append\(', code):
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

def fix_minute_bars(code):
    """
    Replace history_bars(..., '1m', ...) with '1d' in day-frequency strategies.
    Only fix simple close/open/high/low fetches, not complex intraday logic.
    """
    if 'run_daily' not in code and 'run_weekly' not in code:
        return code

    # history_bars(stock, N, '1m', field) → history_bars(stock, N, '1d', field)
    # for field in close/open/high/low/volume
    code = re.sub(
        r"(history_bars\(\w+,\s*\d+,\s*)'1m'(,\s*'(?:close|open|high|low|volume)')",
        r"\g<1>'1d'\2",
        code
    )
    return code

def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        original = f.read()
    code = original
    changes = []

    if re.search(r'\[s\.order_book_id\s+for s in instruments_df', code):
        new = fix_all_instruments_iter(code)
        if new != code:
            code = new
            changes.append('all_instruments_iter')

    if re.search(r'candidates\.append\(', code) and re.search(r'for \w+ in candidates', code):
        new = fix_candidates_self_append(code)
        if new != code:
            code = new
            changes.append('candidates_self_append')

    if re.search(r"history_bars\(\w+,\s*\d+,\s*'1m'", code):
        new = fix_minute_bars(code)
        if new != code:
            code = new
            changes.append('minute_bars')

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
