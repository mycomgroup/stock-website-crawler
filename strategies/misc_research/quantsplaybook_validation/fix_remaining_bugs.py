#!/usr/bin/env python3
"""
修复剩余 bug：
1. all_instruments_iter: [s.order_book_id for s in instruments_df ...] → instruments_df['order_book_id'].tolist()
2. jq_fundamentals_syntax: query(fundamentals...).filter(...) + get_fundamentals(q,...) → get_factor()
3. candidates_self_append (漏网的)
4. undefined_stocks (漏网的)
5. df_append_deprecated: df.append(other) → pd.concat([df, other])
6. undefined_data_var: len(data) → len(data_close)
7. minute_bars: history_bars(..., '1m', ...) in day backtest → use '1d'
"""
import os, re

STRATEGIES_DIR = 'strategies/quantsplaybook_validation/strategies'

# ─────────────────────────────────────────────────────────────────────────────
# Fix 1: all_instruments iterated as objects
# ─────────────────────────────────────────────────────────────────────────────
def fix_all_instruments_iter(code):
    # Pattern: instruments_df = all_instruments('CS')
    #          stock_ids = [s.order_book_id for s in instruments_df if not s.order_book_id.startswith(...)]
    # Fix: stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(...)]
    code = re.sub(
        r'\[s\.order_book_id for s in instruments_df if not s\.order_book_id\.startswith\(([^)]+)\)\]',
        r"[s for s in instruments_df['order_book_id'].tolist() if not s.startswith(\1)]",
        code
    )
    # Also handle: [s.order_book_id for s in instruments_df if not s.order_book_id.startswith(...)]
    # without the 'not' variant
    code = re.sub(
        r'\[s\.order_book_id for s in instruments_df\]',
        r"instruments_df['order_book_id'].tolist()",
        code
    )
    # Remove now-redundant lines like:
    # stock_ids = [s.order_book_id for s in instruments_df if ...]  (already fixed above)
    # But also handle standalone dead lines that reference stock_ids after fix
    return code

# ─────────────────────────────────────────────────────────────────────────────
# Fix 2: JQ fundamentals syntax → get_factor()
# ─────────────────────────────────────────────────────────────────────────────
def fix_jq_fundamentals(code):
    """
    Replace JQ-style:
        q = query(
            fundamentals.eod_derivative_indicator.pb_ratio,
            fundamentals.financial_indicator.roe,
            ...
        ).filter(
            fundamentals.eod_derivative_indicator.order_book_id.in_(stocks)
        ).limit(500)
        df = get_fundamentals(q, entry_date=context.now.date())

    With RiceQuant get_factor():
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe', ...],
            start_date=str(prev_date),
            end_date=str(prev_date)
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
    """

    # Extract factor names from fundamentals.xxx.yyy pattern
    def extract_factors(query_block):
        factors = re.findall(r'fundamentals\.\w+\.\s*(\w+)', query_block)
        # Map common JQ factor names to RiceQuant equivalents
        factor_map = {
            'pb_ratio': 'pb_ratio',
            'pe_ratio': 'pe_ratio',
            'market_cap': 'market_cap',
            'roe': 'roe',
            'roa': 'roa',
            'eps': 'eps',
            'inc_net_profit_year_on_year': 'inc_net_profit_year_on_year',
            'net_profit_margin': 'net_profit_margin',
            'gross_profit_margin': 'gross_profit_margin',
            'dividend_yield': 'dividend_yield',
            'pcf_ratio': 'pcf_ratio',
            'ps_ratio': 'ps_ratio',
            'turnover_ratio': 'turnover_ratio',
            'circulating_market_cap': 'circulating_market_cap',
        }
        mapped = [factor_map.get(f, f) for f in factors if f not in ('order_book_id',)]
        return list(dict.fromkeys(mapped))  # deduplicate preserving order

    # Find the stock variable used in .in_(xxx)
    def extract_stock_var(query_block):
        m = re.search(r'\.in_\((\w+)\)', query_block)
        return m.group(1) if m else 'stocks'

    # Find the indent of the q = query(...) block
    def get_indent(code, pos):
        line_start = code.rfind('\n', 0, pos) + 1
        line = code[line_start:pos]
        return re.match(r'(\s*)', line).group(1)

    # Pattern: q = query(...).filter(...).limit(...) followed by df = get_fundamentals(q, ...)
    # We need to handle multi-line query blocks
    pattern = re.compile(
        r'([ \t]*)(\w+)\s*=\s*query\s*\((.*?)\)\s*\.filter\s*\((.*?)\)\s*(?:\.limit\s*\(\d+\)\s*)?\n'
        r'\s*(\w+)\s*=\s*get_fundamentals\s*\(\s*\2\s*,\s*entry_date\s*=\s*[^\n]+\)',
        re.DOTALL
    )

    def replace_fundamentals(m):
        indent = m.group(1)
        q_var = m.group(2)
        query_body = m.group(3)
        filter_body = m.group(4)
        df_var = m.group(5)

        factors = extract_factors(query_body)
        stock_var = extract_stock_var(filter_body)

        if not factors:
            factors = ['market_cap', 'pb_ratio', 'roe']

        factors_str = ', '.join(f"'{f}'" for f in factors)

        replacement = (
            f"{indent}factor_df = get_factor(\n"
            f"{indent}    {stock_var},\n"
            f"{indent}    [{factors_str}],\n"
            f"{indent}    start_date=str(prev_date),\n"
            f"{indent}    end_date=str(prev_date)\n"
            f"{indent})\n"
            f"{indent}if factor_df is None or len(factor_df) == 0:\n"
            f"{indent}    return\n"
            f"{indent}{df_var} = factor_df.groupby(level=0).last().dropna()"
        )
        return replacement

    code = pattern.sub(replace_fundamentals, code)

    # Also fix: df = df[df['column_name'] > x] where column_name uses old JQ names
    # (usually already correct since we map them above)

    # Fix prev_date if not defined (some files use context.now.date() directly)
    # Ensure prev_date is defined before get_factor calls
    if 'get_factor(' in code and 'prev_date' not in code:
        # Add prev_date definition before get_factor
        code = re.sub(
            r'([ \t]+)(factor_df = get_factor\()',
            r'\1prev_date = context.now.date()\n\1\2',
            code
        )

    return code

# ─────────────────────────────────────────────────────────────────────────────
# Fix 3: df.append(other_df) → pd.concat([df, other_df])
# ─────────────────────────────────────────────────────────────────────────────
def fix_df_append_deprecated(code):
    # all_instruments('LOF').append(all_instruments('ETF'), ignore_index=True)
    code = re.sub(
        r'all_instruments\(([\'"]LOF[\'"])\)\.append\(all_instruments\(([\'"]ETF[\'"])\),\s*ignore_index=True\)',
        r'pd.concat([all_instruments(\1), all_instruments(\2)], ignore_index=True)',
        code
    )
    # Generic df.append(other, ...) → pd.concat([df, other], ...)
    code = re.sub(
        r'(\w+)\.append\((\w+),\s*ignore_index=True\)',
        r'pd.concat([\1, \2], ignore_index=True)',
        code
    )
    return code

# ─────────────────────────────────────────────────────────────────────────────
# Fix 4: undefined_data_var: len(data) → len(data_close)
# ─────────────────────────────────────────────────────────────────────────────
def fix_undefined_data_var(code):
    # if ... len(data) < N where data is not defined but data_close is
    if re.search(r'len\(data\)', code) and re.search(r'data_close', code) and not re.search(r'\bdata\s*=', code):
        code = re.sub(r'\blen\(data\)\b', 'len(data_close)', code)
    return code

# ─────────────────────────────────────────────────────────────────────────────
# Fix 5: candidates self-append (any remaining)
# ─────────────────────────────────────────────────────────────────────────────
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
            # Look ahead for self-append
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

# ─────────────────────────────────────────────────────────────────────────────
# Fix 6: undefined stocks in get_factor
# ─────────────────────────────────────────────────────────────────────────────
def fix_undefined_stocks(code):
    if not re.search(r'get_factor\(\s*stocks\s*,', code):
        return code
    lines = code.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        if re.search(r'get_factor\(\s*stocks\s*,', line):
            context_window = '\n'.join(lines[max(0, i-60):i])
            last_func = context_window.split('def ')[-1]
            if not re.search(r'\bstocks\s*=', last_func):
                for var in ['stock_ids', 'pool', 'list_stock', 'all_stocks', 'valid', 'candidates']:
                    if re.search(rf'\b{var}\s*=', last_func):
                        line = re.sub(r'get_factor\(\s*stocks\s*,', f'get_factor({var},', line)
                        break
        new_lines.append(line)
    return '\n'.join(new_lines)

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        original = f.read()
    code = original
    changes = []

    if re.search(r'\[s\.order_book_id for s in instruments_df', code):
        code = fix_all_instruments_iter(code)
        changes.append('all_instruments_iter')

    if 'get_fundamentals' in code and 'query(' in code:
        code = fix_jq_fundamentals(code)
        changes.append('jq_fundamentals')

    if '.append(all_instruments(' in code or re.search(r'\w+\.append\(\w+,\s*ignore_index=True\)', code):
        code = fix_df_append_deprecated(code)
        changes.append('df_append_deprecated')

    if re.search(r'len\(data\)', code) and re.search(r'data_close', code) and not re.search(r'\bdata\s*=', code):
        code = fix_undefined_data_var(code)
        changes.append('undefined_data_var')

    if re.search(r'candidates\.append\(', code) and re.search(r'for \w+ in candidates', code):
        code = fix_candidates_self_append(code)
        changes.append('candidates_self_append')

    if re.search(r'get_factor\(\s*stocks\s*,', code):
        code = fix_undefined_stocks(code)
        changes.append('undefined_stocks')

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
