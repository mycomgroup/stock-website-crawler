#!/usr/bin/env python3
"""
批量修复导致回测收益为 0 的 bug：
1. factor_len(df) typo → len(df)
2. get_factor(stocks, ...) 中 stocks 未定义 → 用上下文正确变量名
3. weekday() != 0 限制 → 去掉，改为每天运行
4. candidates 自我 append → 用独立 result 列表
5. peg 因子名 → peg_ratio
"""
import os
import re

STRATEGIES_DIR = 'strategies/quantsplaybook_validation/strategies'

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
    
    if code != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return changes
    return []

def main():
    files = sorted([f for f in os.listdir(STRATEGIES_DIR) if f.startswith('rq_') and f.endswith('.py')])
    
    total_fixed = 0
    for fname in files:
        path = os.path.join(STRATEGIES_DIR, fname)
        changes = fix_file(path)
        if changes:
            total_fixed += 1
            print(f'✓ {fname}: {changes}')
    
    print(f'\n共修复 {total_fixed} 个文件')

if __name__ == '__main__':
    main()
