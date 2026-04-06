"""
第二轮修复：处理 get_fundamentals、log.set_level、portfolio_value 等残留问题
"""
import re
import os

base = 'strategies/quantsplaybook_validation/strategies'


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'SKIP_REASON' in content:
        return False

    original = content

    # 1. log.set_level / logger.set_level -> comment out
    content = re.sub(r'^(\s*)log\.set_level\(.*\)', r'\1# log.set_level removed', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)logger\.set_level\(.*\)', r'\1# logger.set_level removed', content, flags=re.MULTILINE)

    # 2. portfolio_value -> total_value
    content = content.replace('portfolio.portfolio_value', 'portfolio.total_value')
    content = content.replace('.portfolio_value', '.total_value')

    # 3. order_target(x, 0) -> order_target_value(x, 0)  (only the zero-quantity clear form)
    content = re.sub(r'\border_target\(([^,]+),\s*0\)', r'order_target_value(\1, 0)', content)

    # 4. get_all_securities in comments/SKIP files - already handled, but catch remaining
    content = re.sub(
        r"get_all_securities\(['\"]stock['\"](?:,\s*[^)]+)?\)",
        "all_instruments('CS')['order_book_id'].tolist()",
        content
    )

    # 5. get_fundamentals with JQ ORM style
    #    Strategy: replace the entire query block with get_factor equivalent
    #    We do a best-effort replacement that wraps it in a comment
    if 'get_fundamentals' in content and 'fundamentals.eod_derivative_indicator' not in content:
        # Find and replace each get_fundamentals call
        # Match: get_fundamentals(q, ...) or get_fundamentals(query(...), ...)
        # Use a bracket-counting approach
        result = []
        i = 0
        while i < len(content):
            # Look for get_fundamentals(
            idx = content.find('get_fundamentals(', i)
            if idx == -1:
                result.append(content[i:])
                break
            result.append(content[i:idx])
            # Find matching closing paren
            depth = 0
            j = idx + len('get_fundamentals(') - 1  # at the opening (
            while j < len(content):
                if content[j] == '(':
                    depth += 1
                elif content[j] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            call = content[idx:j+1]
            # Replace with get_factor placeholder
            replacement = (
                '# [RQ-MIGRATED] get_fundamentals -> use get_factor()\n'
                '# ' + call.replace('\n', '\n    # ') + '\n'
                'pd.DataFrame()  # TODO: implement with get_factor(stocks, factors, date, date)'
            )
            result.append(replacement)
            i = j + 1
        content = ''.join(result)

    # 6. get_price( -> comment (only if it's the JQ-style get_price for fundamentals/nav)
    #    For LOF net value in rq_68, we already rewrote it - skip if already fixed
    if 'get_price(' in content and 'unit_net_value' in content:
        # Already handled in rq_68 rewrite, skip
        pass

    # 7. context.current_dt -> context.now
    content = content.replace('context.current_dt', 'context.now')

    # 8. context.previous_date -> _get_prev_date(context)
    if 'context.previous_date' in content:
        content = content.replace('context.previous_date', '_get_prev_date(context)')
        if 'def _get_prev_date' not in content:
            insert_pos = content.find('\ndef ')
            if insert_pos == -1:
                insert_pos = 0
            helper = '\n\ndef _get_prev_date(context):\n    dates = get_trading_dates(end_date=context.now.date(), count=2)\n    return dates[0] if len(dates) >= 2 else context.now.date()\n'
            content = content[:insert_pos] + helper + content[insert_pos:]

    # 9. Add handle_bar if missing and scheduler is used
    if 'def handle_bar' not in content and ('scheduler.run_daily' in content or 'scheduler.run_weekly' in content or 'scheduler.run_monthly' in content):
        init_end = content.find('\ndef ', content.find('def init('))
        if init_end != -1:
            content = content[:init_end] + '\n\ndef handle_bar(context, bar_dict):\n    pass\n' + content[init_end:]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


if __name__ == '__main__':
    files = sorted([f for f in os.listdir(base) if f.endswith('.py')])
    fixed = []
    for f in files:
        if fix_file(os.path.join(base, f)):
            fixed.append(f)
    print(f'Fixed: {len(fixed)}')
    for f in fixed:
        print(f'  {f}')
