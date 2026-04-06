#!/usr/bin/env python3
"""
Batch fix: Replace JoinQuant fundamentals ORM with RiceQuant get_factor() API
"""
import os, re

STRAT_DIR = os.path.join(os.path.dirname(__file__), "strategies")

FACTOR_MAP = {
    'pe_ratio': 'pe_ratio',
    'pb_ratio': 'pb_ratio',
    'market_cap': 'market_cap',
    'ps_ratio': 'ps_ratio',
    'pcf_ratio': 'pcf_ratio',
    'dividend_yield': 'dividend_yield',
    'ev': 'ev',
    'roe': 'roe',
    'roa': 'roa',
    'inc_net_profit_year_on_year': 'inc_net_profit_year_on_year',
    'inc_revenue_year_on_year': 'inc_revenue_year_on_year',
    'gross_profit_margin': 'gross_profit_margin',
    'net_profit_margin': 'net_profit_margin',
    'eps': 'eps',
    'revenue': 'revenue',
    'net_profit': 'net_profit',
    'total_assets': 'total_assets',
    'equity': 'equity',
    'operating_cash_flow': 'operating_cash_flow',
    'research_and_development_costs': 'research_and_development_costs',
    'turnover_ratio': 'turnover_ratio',
    'a_share_market_val': 'market_cap',
}

PCT_FACTORS = {
    'roe', 'roa', 'inc_net_profit_year_on_year', 'inc_revenue_year_on_year',
    'gross_profit_margin', 'net_profit_margin',
}

def find_query_blocks(content):
    blocks = []
    for m in re.finditer(r'(\s*)q\s*=\s*query\s*\(', content):
        start = m.start()
        # count indent of this line
        line_start = content.rfind('\n', 0, start) + 1
        indent = start - line_start

        pos = m.end() - 1
        depth = 1
        while pos < len(content) - 1 and depth > 0:
            pos += 1
            if content[pos] == '(':
                depth += 1
            elif content[pos] == ')':
                depth -= 1

        rest = content[pos+1:]
        gf_match = re.search(r'[ \t]*df\s*=\s*get_fundamentals\([^)]*\)', rest)
        if gf_match:
            end = pos + 1 + gf_match.end()
            blocks.append((start, end, indent, content[start:end]))
    return blocks

def extract_factors(block):
    factors = []
    for jq_name, rq_name in FACTOR_MAP.items():
        if f'.{jq_name}' in block:
            if rq_name not in factors:
                factors.append(rq_name)
    return factors

def extract_filter_conditions(block):
    conditions = []
    filter_match = re.search(r'\.filter\((.*?)(?=\)\s*\.order_by|\)\s*\.limit|\)\s*\n)', block, re.DOTALL)
    if not filter_match:
        return conditions
    filter_text = filter_match.group(1)
    for line in filter_text.split('\n'):
        line = line.strip().rstrip(',')
        if not line or 'fundamentals.' not in line or '.in_(' in line:
            continue
        m = re.search(r'fundamentals\.\w+\.(\w+)\s*([><=!]+)\s*([\d.]+)', line)
        if m:
            factor, op, val = m.group(1), m.group(2), float(m.group(3))
            rq_name = FACTOR_MAP.get(factor, factor)
            if rq_name == 'market_cap':
                conditions.append(f"df['{rq_name}'] {op} {val * 1e8:.0f}")
            elif rq_name in PCT_FACTORS and val > 1:
                conditions.append(f"df['{rq_name}'] {op} {val / 100}")
            else:
                conditions.append(f"df['{rq_name}'] {op} {val}")
    return conditions

def extract_sort(block):
    m = re.search(r'\.order_by\(fundamentals\.\w+\.(\w+)(?:\.(asc|desc)\(\))?\)', block)
    if m:
        rq_name = FACTOR_MAP.get(m.group(1), m.group(1))
        return rq_name, (m.group(2) or 'asc') == 'asc'
    return None, True

def extract_limit(block):
    m = re.search(r'\.limit\(([^)]+)\)', block)
    return m.group(1).strip() if m else None

def build_replacement(factors, conditions, sort_col, sort_asc, limit, indent):
    s = ' ' * indent
    factor_list = ', '.join(f"'{f}'" for f in factors)
    lines = [
        "prev_date = get_trading_dates(end_date=context.now.date(), count=2)[0]",
        "factor_df = get_factor(",
        f"    stocks,",
        f"    [{factor_list}],",
        "    start_date=str(prev_date),",
        "    end_date=str(prev_date)",
        ")",
        "if factor_df is None or factor_df.empty:",
        "    return",
        "df = factor_df.groupby(level=0).last().dropna()",
    ]
    for cond in conditions:
        lines.append(f"df = df[{cond}]")
    if sort_col:
        lines.append(f"df = df.sort_values('{sort_col}', ascending={sort_asc})")
    if limit:
        lines.append(f"df = df.head({limit})")
    lines.append("candidates = df.index.tolist()")
    return '\n'.join(s + l for l in lines)

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'fundamentals.' not in content:
        return False, "skip"
    blocks = find_query_blocks(content)
    if not blocks:
        return False, "no query blocks"
    new_content = content
    for start, end, indent, block in reversed(blocks):
        factors = extract_factors(block)
        if not factors:
            continue
        conditions = extract_filter_conditions(block)
        sort_col, sort_asc = extract_sort(block)
        limit = extract_limit(block)
        replacement = build_replacement(factors, conditions, sort_col, sort_asc, limit, indent)
        new_content = new_content[:start] + '\n' + replacement + new_content[end:]
    if new_content != content:
        # clean up leftover lines
        new_content = re.sub(r'[ \t]*df\.columns\s*=\s*\[c\.split\([^)]+\)\[-1\] for c in df\.columns\]\n', '', new_content)
        new_content = re.sub(r'[ \t]*df\s*=\s*df\.set_index\([\'"]order_book_id[\'"]\)\n', '', new_content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"{len(blocks)} block(s)"
    return False, "no change"

files = sorted([
    os.path.join(STRAT_DIR, f)
    for f in os.listdir(STRAT_DIR)
    if f.startswith('rq_') and f.endswith('.py')
])

fixed, failed = [], []
for fpath in files:
    fname = os.path.basename(fpath)
    try:
        ok, msg = fix_file(fpath)
        if ok:
            fixed.append(fname)
            print(f"✓ {fname}: {msg}")
        elif msg not in ("skip",):
            print(f"  {fname}: {msg}")
    except Exception as e:
        failed.append((fname, str(e)))
        print(f"✗ {fname}: {e}")

print(f"\n=== Fixed: {len(fixed)}, Failed: {len(failed)} ===")
for f, e in failed:
    print(f"  FAILED: {f}: {e}")
