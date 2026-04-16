#!/usr/bin/env python3
"""
批量修复导致回测收益为 0 的 bug：
1. factor_len(df) typo → len(df)
2. get_factor(stocks, ...) 中 stocks 未定义 → 用上下文正确变量名
3. weekday() != 0 限制 → 去掉，改为每天运行
4. candidates 自我 append → 用独立 result 列表
5. peg 因子名 → peg_ratio
6. get_factor 结果索引层级归一化，避免候选集被清空
7. 放宽 bar_dict 缺失时的交易过滤，避免静默空跑
8. 周期标记延后到实际调仓前，避免本月/本周提前锁死
"""
import os
import re
from pathlib import Path

STRATEGIES_DIR = 'strategies/quantsplaybook_validation/strategies'
RESULTS_FILE = 'strategies/quantsplaybook_validation/NEW_STRATEGY_RESULTS.md'

FACTOR_HELPER = '''
def _normalize_factor_frame(factor_df):
    if factor_df is None:
        return None
    try:
        if hasattr(factor_df, 'empty') and factor_df.empty:
            return factor_df
        if not hasattr(factor_df, 'columns'):
            factor_df = factor_df.to_frame()
        index = getattr(factor_df, 'index', None)
        if index is not None and getattr(index, 'nlevels', 1) > 1:
            factor_df = factor_df.groupby(level=-1).last()
        return factor_df.dropna()
    except Exception:
        return None


'''.lstrip()


def get_zero_return_files():
    results_path = Path(RESULTS_FILE)
    if not results_path.exists():
        return None

    target_files = []
    for line in results_path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| rq_'):
            continue
        cols = [col.strip() for col in line.split('|') if col.strip()]
        if len(cols) < 9:
            continue
        filename = cols[0]
        local_exists = cols[1]
        fetch_status = cols[6]
        total_return = cols[8]
        if local_exists != '✅':
            continue
        if fetch_status != '✅ 完成':
            continue
        if total_return != '0.00%':
            continue
        target_files.append(filename)
    return sorted(set(target_files))


def fix_factor_len_typo(code):
    """factor_len(df) → len(df)"""
    return code.replace('factor_len(df)', 'len(df)')

def fix_weekday_bug(code):
    """去掉 weekday() != 0 限制"""
    # Pattern: if context.now.weekday() != 0 or today == context.last_week_date:
    code = re.sub(
        r'if context\.now\.weekday\(\) != 0 or today == context\.last_week_date:\s*\n(\s+)return',
        r'if today == context.last_week_date:\n\1return',
        code
    )
    return code

def fix_peg_factor_name(code):
    """'peg' → 'peg_ratio' in get_factor calls"""
    # Only replace 'peg' as a standalone factor name in lists
    code = re.sub(r"'peg'", "'peg_ratio'", code)
    # Also fix df['peg'] and df.at[stock, 'peg'] etc
    code = re.sub(r"\[(['\"])peg\1\]", r"['\1peg_ratio\1']", code)
    code = re.sub(r"at\[stock, (['\"])peg\1\]", r"at[stock, \1peg_ratio\1]", code)
    return code

def fix_candidates_self_append(code):
    """
    Fix pattern where candidates list is iterated and appended to simultaneously.
    Replace with a separate result list.
    """
    # Find the pattern: for stock in candidates: ... candidates.append(stock)
    # We need to:
    # 1. Add result = [] before the for loop
    # 2. Replace candidates.append(stock) with result.append(stock)
    # 3. Replace context.candidates = candidates[...] with context.candidates = result[...]

    # Pattern: variable name for the loop target list
    # Look for: `    for stock in candidates:` followed eventually by `candidates.append(`
    
    lines = code.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect start of a for-loop over candidates that also appends
        if re.match(r'(\s+)for stock in candidates:', line):
            indent = re.match(r'(\s+)', line).group(1)
            # Look ahead to see if there's a candidates.append within this block
            block_end = i + 1
            has_self_append = False
            while block_end < len(lines):
                bl = lines[block_end]
                # Check if we've left the block (dedented or empty line followed by dedent)
                if bl.strip() and not bl.startswith(indent + ' ') and not bl.startswith(indent + '\t'):
                    break
                if 'candidates.append(' in bl:
                    has_self_append = True
                block_end += 1
            
            if has_self_append:
                # Insert `result = []` before the for loop
                new_lines.append(indent + 'result = []')
                # Add the for loop line
                new_lines.append(line)
                i += 1
                # Process the block, replacing candidates.append with result.append
                while i < block_end:
                    bl = lines[i]
                    bl = bl.replace('candidates.append(stock)', 'result.append(stock)')
                    bl = bl.replace('candidates.append((stock,', 'result.append((stock,')
                    new_lines.append(bl)
                    i += 1
                continue
        new_lines.append(line)
        i += 1
    
    code = '\n'.join(new_lines)
    
    # Now fix the final assignment: context.candidates = candidates[:...] → result[:...]
    # But only if we made the above change (result list was introduced)
    if 'result = []' in code:
        code = re.sub(
            r'context\.candidates = candidates\[:(.*?)\]',
            r'context.candidates = result[:\1]',
            code
        )
        # Also handle: context.candidates = [s for s, _ in candidates[:...]]
        # These are tuple-based, leave as-is since we changed append to result.append((stock,...))
        code = re.sub(
            r'context\.candidates = \[s for s, _ in candidates\[:(.*?)\]\]',
            r'context.candidates = [s for s, _ in result[:\1]]',
            code
        )
    
    return code

def fix_undefined_stocks_in_get_factor(code):
    """
    Fix get_factor(stocks, ...) where stocks is not defined in scope.
    Determine the correct variable from context.
    """
    lines = code.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Find get_factor(stocks, ...) calls
        if re.search(r'get_factor\(\s*stocks\s*,', line):
            # Look backwards to find what variable holds the stock list
            # Common patterns: pool, list_stock, candidates, all_stocks, stock_ids
            context_window = '\n'.join(lines[max(0, i-50):i])
            
            replacement = None
            # Check what variable was defined most recently before this line
            for var in ['pool', 'list_stock', 'all_stocks', 'stock_ids', 'valid']:
                if re.search(rf'\b{var}\s*=', context_window):
                    replacement = var
                    break
            
            if replacement:
                line = re.sub(r'get_factor\(\s*stocks\s*,', f'get_factor({replacement},', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)


def ensure_factor_helper(code):
    if '_normalize_factor_frame(' in code:
        return code

    lines = code.splitlines(keepends=True)
    insert_at = 0
    while insert_at < len(lines):
        stripped = lines[insert_at].strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            insert_at += 1
            continue
        if stripped == '':
            insert_at += 1
            continue
        break
    lines.insert(insert_at, FACTOR_HELPER)
    return ''.join(lines)


def fix_factor_groupby_normalization(code):
    pattern = re.compile(
        r'^(?P<indent>\s*)(?P<lhs>\w+)\s*=\s*(?P<src>\w+)\.groupby\(level=(?:0|-1)\)\.last\(\)\.dropna\(\)\s*$',
        re.MULTILINE,
    )
    if not pattern.search(code):
        return code

    code = ensure_factor_helper(code)
    return pattern.sub(r'\g<indent>\g<lhs> = _normalize_factor_frame(\g<src>)', code)


def relax_bar_dict_filters(code):
    lines = code.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        future_window = '\n'.join(lines[idx + 1: idx + 8])
        bar_used_later = re.search(r'\bbar\.(open|close|high|low|limit_up|limit_down|last)\b', future_window)

        if stripped == 'if bar is not None and bar.is_trading:' and not bar_used_later:
            lines[idx] = line.replace('if bar is not None and bar.is_trading:', 'if bar is None or bar.is_trading:')
            continue

        if stripped == 'if bar is None or not bar.is_trading:' and not bar_used_later:
            lines[idx] = line.replace('if bar is None or not bar.is_trading:', 'if bar is not None and not bar.is_trading:')

    code = '\n'.join(lines)
    code = re.sub(
        r'\(bar_dict\[(?P<var>[A-Za-z_][A-Za-z0-9_]*)\] if (?P=var) in bar_dict else None\) and bar_dict\[(?P=var)\]\.is_trading',
        r'(\g<var> not in bar_dict) or bar_dict[\g<var>].is_trading',
        code,
    )
    return code


def delay_period_markers(code):
    lines = code.splitlines()
    changed = False

    for period in ('week', 'month', 'quarter'):
        current_var = f'current_{period}'
        assign_line = f'context.{period} = {current_var}'

        for idx, line in enumerate(lines):
            if line.strip() != assign_line:
                continue

            indent = line[: len(line) - len(line.lstrip())]
            if not indent:
                continue

            guard_idx = None
            for j in range(max(0, idx - 6), idx):
                if lines[j].strip() == f'if {current_var} == context.{period}:':
                    guard_idx = j
                    break
            if guard_idx is None:
                continue

            guard_indent = lines[guard_idx][: len(lines[guard_idx]) - len(lines[guard_idx].lstrip())]
            if indent != guard_indent:
                continue

            return_idx = guard_idx + 1
            while return_idx < len(lines) and lines[return_idx].strip() == '':
                return_idx += 1
            if return_idx >= len(lines) or lines[return_idx].strip() != 'return':
                continue

            insert_idx = None
            for j in range(idx + 1, len(lines)):
                stripped = lines[j].strip()
                line_indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
                if line_indent == guard_indent and stripped.startswith('if not ') and j + 1 < len(lines):
                    next_idx = j + 1
                    while next_idx < len(lines) and lines[next_idx].strip() == '':
                        next_idx += 1
                    if next_idx < len(lines) and lines[next_idx].strip() == 'return':
                        insert_idx = next_idx + 1
                if line_indent == guard_indent and (
                    stripped.startswith('for ') and 'context.portfolio.positions.keys()' in stripped
                    or stripped.startswith('order_target_value(')
                    or stripped.startswith('order_to(')
                    or stripped.startswith('weight =')
                ):
                    if insert_idx is None:
                        insert_idx = j
                    break

            if insert_idx is None or insert_idx <= idx:
                continue

            moved_line = lines.pop(idx)
            if insert_idx > idx:
                insert_idx -= 1
            lines.insert(insert_idx, moved_line)
            changed = True
            break

    return '\n'.join(lines) + ('\n' if code.endswith('\n') else '') if changed else code

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    code = original
    changes = []
    
    if 'factor_len(df)' in code:
        code = fix_factor_len_typo(code)
        changes.append('factor_len_typo')
    
    if 'weekday() != 0' in code:
        code = fix_weekday_bug(code)
        changes.append('weekday_bug')
    
    if "'peg'" in code and 'peg_ratio' not in code:
        code = fix_peg_factor_name(code)
        changes.append('peg_factor_name')
    
    # Check candidates self-append
    if re.search(r'candidates\.append\(stock\)', code) and re.search(r'for stock in candidates', code):
        code = fix_candidates_self_append(code)
        changes.append('candidates_self_append')
    
    # Fix undefined stocks in get_factor (after other fixes)
    if re.search(r'get_factor\(\s*stocks\s*,', code):
        code = fix_undefined_stocks_in_get_factor(code)
        changes.append('undefined_stocks_in_get_factor')

    normalized = fix_factor_groupby_normalization(code)
    if normalized != code:
        code = normalized
        changes.append('factor_groupby_normalization')

    relaxed = relax_bar_dict_filters(code)
    if relaxed != code:
        code = relaxed
        changes.append('relax_bar_dict_filters')

    delayed = delay_period_markers(code)
    if delayed != code:
        code = delayed
        changes.append('delay_period_markers')
    
    if code != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return changes
    return []

def main():
    all_files = sorted([f for f in os.listdir(STRATEGIES_DIR) if f.startswith('rq_') and f.endswith('.py')])
    zero_return_files = get_zero_return_files()
    target_files = [f for f in all_files if zero_return_files is None or f in zero_return_files]
    
    total_fixed = 0
    print(f'扫描文件: {len(target_files)} / {len(all_files)}')
    if zero_return_files is not None:
        print(f'仅修复当前 0.00% 且本地存在的策略文件')

    for fname in target_files:
        path = os.path.join(STRATEGIES_DIR, fname)
        changes = fix_file(path)
        if changes:
            total_fixed += 1
            print(f'✓ {fname}: {changes}')
    
    print(f'\n共修复 {total_fixed} 个文件')

if __name__ == '__main__':
    main()
