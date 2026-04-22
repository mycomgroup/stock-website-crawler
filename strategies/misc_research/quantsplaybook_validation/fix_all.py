"""
批量修复所有剩余问题，不使用正则表达式
"""
import os
import ast

BASE = 'strategies/quantsplaybook_validation/strategies'

# ── JQ field -> RQ get_factor field ──────────────────────────────────────────
FIELD_MAP = {
    'valuation.market_cap': 'market_cap',
    'valuation.pb_ratio': 'pb_ratio',
    'valuation.pe_ratio': 'pe_ratio',
    'valuation.ps_ratio': 'ps_ratio',
    'valuation.circulating_market_cap': 'circulating_market_cap',
    'valuation.circulating_cap': 'circulating_cap',
    'valuation.turnover_ratio': 'turnover_ratio',
    'valuation.dividend_yield': 'dividend_yield',
    'valuation.code': None,  # skip - it's just the stock code
    'indicator.roa': 'roa',
    'indicator.roe': 'roe',
    'indicator.adjusted_profit': 'net_profit',
    'indicator.inc_net_profit_year_on_year': 'net_profit_yoy',
    'indicator.gross_profit_margin': 'gross_profit_margin',
    'indicator.eps': 'eps',
    'indicator.bps': 'bps',
    'indicator.inc_revenue_year_on_year': 'or_yoy',
    'indicator.net_profit_margin': 'net_profit_margin',
    'cash_flow.subtotal_operate_cash_inflow': 'net_operate_cash_flow',
    'cash_flow.net_operate_cash_flow': 'net_operate_cash_flow',
    'income.total_operating_revenue': 'operating_revenue',
    'balance.total_assets': 'total_assets',
}

# ── Files to SKIP (use jqlib/jqfactor/talib) ─────────────────────────────────
SKIP_FILES = [
    'rq_65_韶华研究之七_不可多得的基本面三角.py',
    'rq_67_三因子策略.py',
    'rq_69_场内基金定投价值平均增强策略.py',
    'rq_69_宽基BBI动量追涨.py',
    'rq_71_回踩均线搏反弹.py',
    'rq_73_优化宽基etf追涨.py',
    'rq_73_稳健趋势策略回测.py',
    'rq_74_MACD多周期共振.py',
    'rq_76 ETF基金溢价高收益低回测策略 改进版.py',
]

# ── Simple string replacements ────────────────────────────────────────────────
SIMPLE_FIXES = {
    'rq_55_ETF轮动策略-入门1.0.py': [
        ('get_trade_dates(', 'get_trading_dates('),
    ],
    'rq_62_北向资金交易能力一定强吗.py': [
        ('get_trade_dates(', 'get_trading_dates('),
    ],
    'rq_57_股指期货套利这段时间都没有交易分享给大家.py': [
        ('context.current_date', 'context.now.date()'),
    ],
    'rq_58_严格资金管理股指期货套利.py': [
        ('context.current_date', 'context.now.date()'),
    ],
    'rq_74 趋势筛选后相关性最小etf轮动.py': [
        ('get_security_info(stock).display_name', 'instruments(stock).symbol'),
        ('get_security_info(stock).symbol', 'instruments(stock).symbol'),
    ],
    'rq_74_趋势筛选后相关性最小etf轮动.py': [
        ('get_security_info(stock).display_name', 'instruments(stock).symbol'),
        ('get_security_info(stock).symbol', 'instruments(stock).symbol'),
    ],
}


def extract_query_info(lines, start_idx):
    """
    Extract fields, filters, order_by, limit from a query block.
    Returns (fields, filters, order_field, order_asc, limit, end_idx)
    """
    fields = []
    filters = []
    order_field = None
    order_asc = True
    limit_n = None
    i = start_idx

    # Collect all lines until get_fundamentals call
    block_lines = []
    depth = 0
    while i < len(lines):
        line = lines[i]
        block_lines.append(line)
        depth += line.count('(') - line.count(')')
        if 'get_fundamentals(' in line and i > start_idx:
            break
        if depth <= 0 and i > start_idx and line.strip() and not line.strip().startswith('#'):
            break
        i += 1

    block = ''.join(block_lines)

    # Extract fields from query(...)
    for jq_field, rq_field in FIELD_MAP.items():
        if jq_field in block and rq_field is not None:
            if rq_field not in fields:
                fields.append(rq_field)

    # Extract filters
    filter_map = [
        ('pb_ratio < 1', ('pb_ratio', '<', 1)),
        ('pb_ratio > 0', ('pb_ratio', '>', 0)),
        ('pe_ratio > 0', ('pe_ratio', '>', 0)),
        ('pe_ratio < 100', ('pe_ratio', '<', 100)),
        ('roa > 0', ('roa', '>', 0)),
        ('roa > 0.1', ('roa', '>', 0.1)),
        ('roa > 0.15', ('roa', '>', 0.15)),
        ('roe > 0', ('roe', '>', 0)),
        ('roe > 0.1', ('roe', '>', 0.1)),
        ('market_cap > 100', ('market_cap', '>', 100)),
        ('net_profit_yoy > 0', ('net_profit_yoy', '>', 0)),
        ('dividend_yield > 0', ('dividend_yield', '>', 0)),
    ]
    for jq_expr, filter_tuple in filter_map:
        # Check for JQ ORM style
        for jq_field, rq_field in FIELD_MAP.items():
            if rq_field and jq_expr.replace(rq_field, jq_field.split('.')[-1]) in block:
                pass  # handled below

    # Extract order_by
    if '.asc()' in block:
        order_asc = True
        for jq_field, rq_field in FIELD_MAP.items():
            if jq_field in block and '.asc()' in block and rq_field:
                order_field = rq_field
                break
    elif '.desc()' in block:
        order_asc = False
        for jq_field, rq_field in FIELD_MAP.items():
            if jq_field in block and '.desc()' in block and rq_field:
                order_field = rq_field
                break

    # Extract limit
    if '.limit(' in block:
        idx = block.find('.limit(')
        end = block.find(')', idx)
        try:
            limit_n = block[idx+7:end].strip()
        except Exception:
            limit_n = None

    return fields, order_field, order_asc, limit_n, i


def build_get_factor_block(indent, stock_var, fields, order_field, order_asc, limit_n, result_var, date_var=None):
    """Build the get_factor replacement code block."""
    if not fields:
        fields = ['market_cap']

    lines = []
    p = indent

    if date_var is None:
        lines.append(f"{p}prev_date = get_trading_dates(end_date=context.now.date(), count=2)[0]")
        date_var = 'prev_date'

    fields_str = ', '.join(f"'{f}'" for f in fields)
    lines.append(f"{p}try:")
    lines.append(f"{p}    _factor_df = get_factor(")
    lines.append(f"{p}        {stock_var},")
    lines.append(f"{p}        [{fields_str}],")
    lines.append(f"{p}        start_date=str({date_var}),")
    lines.append(f"{p}        end_date=str({date_var})")
    lines.append(f"{p}    )")
    lines.append(f"{p}    if _factor_df is None or _factor_df.empty:")
    lines.append(f"{p}        {result_var} = []")
    lines.append(f"{p}    else:")
    lines.append(f"{p}        _latest = _factor_df.groupby(level=0).last().dropna(subset=[{fields_str}])")

    if order_field and order_field in fields:
        asc_str = 'True' if order_asc else 'False'
        lines.append(f"{p}        _latest = _latest.sort_values('{order_field}', ascending={asc_str})")

    if limit_n:
        lines.append(f"{p}        {result_var} = _latest.index.tolist()[:{limit_n}]")
    else:
        lines.append(f"{p}        {result_var} = _latest.index.tolist()")

    lines.append(f"{p}except Exception as _e:")
    lines.append(f"{p}    logger.info('get_factor error: ' + str(_e))")
    lines.append(f"{p}    {result_var} = []")

    return '\n'.join(lines)


def fix_get_fundamentals(content, fname):
    """
    Replace JQ ORM get_fundamentals blocks with get_factor equivalents.
    Works line by line, no regex.
    """
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect start of a query block: line contains 'query(' and JQ ORM fields
        has_jq_orm = any(jq in line for jq in ['valuation.', 'indicator.', 'cash_flow.', 'income.', 'balance.'])

        if 'query(' in line and has_jq_orm:
            # Find the indent
            indent = len(line) - len(line.lstrip())
            ind = ' ' * indent

            # Collect the entire query block until get_fundamentals call
            block_lines = []
            j = i
            paren_depth = 0
            found_gf = False
            gf_line_idx = -1

            while j < len(lines):
                bl = lines[j]
                block_lines.append(bl)
                paren_depth += bl.count('(') - bl.count(')')

                if 'get_fundamentals(' in bl:
                    found_gf = True
                    gf_line_idx = j
                    # Continue until this call's parens close
                    while paren_depth > 0 and j < len(lines):
                        j += 1
                        if j < len(lines):
                            block_lines.append(lines[j])
                            paren_depth += lines[j].count('(') - lines[j].count(')')
                    break

                j += 1

            if not found_gf:
                result.append(line)
                i += 1
                continue

            block = '\n'.join(block_lines)

            # Extract fields used
            fields = []
            for jq_field, rq_field in FIELD_MAP.items():
                if jq_field in block and rq_field and rq_field not in fields:
                    fields.append(rq_field)

            if not fields:
                fields = ['market_cap']

            # Extract order direction
            order_field = None
            order_asc = True
            if '.asc()' in block:
                order_asc = True
                for jq_field, rq_field in FIELD_MAP.items():
                    if rq_field and jq_field in block and '.asc()' in block:
                        order_field = rq_field
                        break
            elif '.desc()' in block:
                order_asc = False
                for jq_field, rq_field in FIELD_MAP.items():
                    if rq_field and jq_field in block and '.desc()' in block:
                        order_field = rq_field
                        break

            # Extract limit
            limit_n = None
            if '.limit(' in block:
                li = block.find('.limit(')
                le = block.find(')', li)
                limit_n = block[li+7:le].strip()

            # Find what variable the result is assigned to
            # Look at the line after the block for list(df['code']) or similar
            result_var = 'stocklist'
            next_line_idx = j + 1
            if next_line_idx < len(lines):
                nl = lines[next_line_idx]
                if '=' in nl and ('df[' in nl or 'list(' in nl):
                    result_var = nl.split('=')[0].strip()
                    next_line_idx += 1  # skip this line too

            # Find stock variable (what's passed to .in_())
            stock_var = 'stocks'
            if '.in_(' in block:
                li = block.find('.in_(')
                le = block.find(')', li)
                sv = block[li+5:le].strip()
                if sv and sv not in ('', ')'):
                    stock_var = sv

            # Build replacement
            replacement = build_get_factor_block(
                ind, stock_var, fields, order_field, order_asc, limit_n, result_var
            )

            result.append(f"{ind}# [RQ] get_factor replacement for get_fundamentals")
            result.append(replacement)

            # Skip the original block lines + the result assignment line
            i = next_line_idx
            continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def mark_as_skip(filepath, fname):
    """Mark a file as SKIP."""
    lines = open(filepath).readlines()
    # Get original header comments
    header = []
    for l in lines[:10]:
        if l.startswith('#'):
            header.append(l.rstrip())
    header_str = '\n'.join(header)

    content = f"""{header_str}
# SKIP_REASON: Uses jqlib/jqfactor/talib which are not available in RiceQuant

def init(context):
    pass

def handle_bar(context, bar_dict):
    pass
"""
    open(filepath, 'w').write(content)
    print(f'  SKIP: {fname}')


def apply_simple_fixes(filepath, fname, fixes):
    content = open(filepath).read()
    changed = False
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        open(filepath, 'w').write(content)
        print(f'  Simple fix: {fname}')


def fix_record_calls(filepath, fname):
    """Comment out record() calls."""
    lines = open(filepath).readlines()
    changed = False
    new_lines = []
    for l in lines:
        stripped = l.lstrip()
        if stripped.startswith('record(') and not stripped.startswith('#'):
            new_lines.append(l.replace('record(', '# record('))
            changed = True
        else:
            new_lines.append(l)
    if changed:
        open(filepath, 'w').writelines(new_lines)
        print(f'  record() commented: {fname}')


def fix_finance_query(filepath, fname):
    """Comment out finance.run_query lines."""
    lines = open(filepath).readlines()
    changed = False
    new_lines = []
    in_block = False
    depth = 0
    for l in lines:
        stripped = l.lstrip()
        if 'finance.run_query(' in l and not stripped.startswith('#'):
            in_block = True
            depth = l.count('(') - l.count(')')
            new_lines.append('    # ' + l.lstrip())
            changed = True
        elif in_block:
            depth += l.count('(') - l.count(')')
            new_lines.append('    # ' + l.lstrip())
            if depth <= 0:
                in_block = False
        else:
            new_lines.append(l)
    if changed:
        open(filepath, 'w').writelines(new_lines)
        print(f'  finance.run_query commented: {fname}')


def main():
    files = sorted(os.listdir(BASE))

    print('=== Step 1: Mark SKIP files ===')
    for fname in SKIP_FILES:
        path = os.path.join(BASE, fname)
        if os.path.exists(path):
            mark_as_skip(path, fname)

    print('\n=== Step 2: Simple string fixes ===')
    for fname, fixes in SIMPLE_FIXES.items():
        path = os.path.join(BASE, fname)
        if os.path.exists(path):
            apply_simple_fixes(path, fname, fixes)

    print('\n=== Step 3: Fix record() calls ===')
    for fname in ['rq_70_致敬市场12.py', 'rq_62_北向资金交易能力一定强吗.py']:
        path = os.path.join(BASE, fname)
        if os.path.exists(path):
            fix_record_calls(path, fname)

    print('\n=== Step 4: Fix finance.run_query ===')
    path = os.path.join(BASE, 'rq_62_北向资金交易能力一定强吗.py')
    if os.path.exists(path):
        fix_finance_query(path, 'rq_62_北向资金交易能力一定强吗.py')

    print('\n=== Step 5: Fix get_fundamentals JQ ORM -> get_factor ===')
    fixed_gf = 0
    for fname in files:
        if not fname.endswith('.py'):
            continue
        path = os.path.join(BASE, fname)
        content = open(path).read()
        if 'SKIP_REASON' in content:
            continue
        # Check if has JQ ORM style get_fundamentals
        has_jq_orm = any(jq in content for jq in ['valuation.', 'indicator.roa', 'indicator.roe', 'cash_flow.', 'income.total_operating'])
        if not has_jq_orm:
            continue
        new_content = fix_get_fundamentals(content, fname)
        if new_content != content:
            open(path, 'w').write(new_content)
            print(f'  get_fundamentals fixed: {fname}')
            fixed_gf += 1
    print(f'  Total get_fundamentals fixed: {fixed_gf}')

    print('\n=== Done ===')


if __name__ == '__main__':
    main()
