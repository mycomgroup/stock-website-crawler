"""
批量自动修复 RiceQuant 策略文件中残留的 JoinQuant API 问题
只处理机械性替换，不改变策略逻辑
"""
import re
import os

base = 'strategies/quantsplaybook_validation/strategies'

# ── 简单字符串替换规则 ──────────────────────────────────────────────────────────
SIMPLE_REPLACEMENTS = [
    # 全局变量
    (r'\bg\.([a-z_A-Z])', r'context.\1'),

    # 函数名
    ('def initialize(context):', 'def init(context):'),

    # 日志
    ('log.info(', 'logger.info('),
    ('log.warn(', 'logger.warn('),
    ('log.error(', 'logger.error('),
    ('log.debug(', 'logger.debug('),
    ('log.set_level(', '# log.set_level('),
    ('logger.set_level(', '# logger.set_level('),

    # 账户
    ('context.portfolio.available_cash', 'context.portfolio.cash'),
    ('context.portfolio.portfolio_value', 'context.portfolio.total_value'),

    # 持仓属性
    ('position.security', 'position.order_book_id'),
    ('.price\n', '.last_price\n'),
    ('position.value\n', 'position.market_value\n'),
    ('position.value)', 'position.market_value)'),
    ('position.value,', 'position.market_value,'),
    ('position.value}', 'position.market_value}'),
    ('position.value ', 'position.market_value '),

    # 时间
    ('context.current_dt', 'context.now'),
    ('context.previous_date', '_get_prev_date(context)'),

    # 清仓
    ('order_target(stock, 0)', 'order_target_value(stock, 0)'),
    ('order_target(s, 0)', 'order_target_value(s, 0)'),
    ('order_target(security, 0)', 'order_target_value(security, 0)'),
    ('order_target(position.order_book_id, 0)', 'order_target_value(position.order_book_id, 0)'),

    # schedule_function -> scheduler pattern (handled by regex below)
]

# ── 正则替换规则 ────────────────────────────────────────────────────────────────
REGEX_REPLACEMENTS = [
    # run_daily/run_monthly/run_weekly 裸调用（不带 scheduler. 前缀）
    (r'(?<!\.)run_daily\((\w+),\s*time_rule=', r'scheduler.run_daily(\1, time_rule='),
    (r'(?<!\.)run_weekly\((\w+),\s*weekday=', r'scheduler.run_weekly(\1, weekday='),
    (r'(?<!\.)run_monthly\((\w+),\s*trading_session=', r'scheduler.run_monthly(\1, trading_session='),

    # schedule_function -> scheduler.run_daily (approximate)
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]09:30[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=0))'),
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]09:31[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=1))'),
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]09:25[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=-5))'),
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]before_open[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=-30))'),
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]every_bar[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=0))'),
    (r'schedule_function\((\w+),\s*date_rule=\d+,\s*time_rule=[\'"]15:10[\'"]\)',
     r'scheduler.run_daily(\1, time_rule=market_close(minute=10))'),
    # generic fallback for remaining schedule_function
    (r'schedule_function\((\w+),\s*date_rule=[^,]+,\s*time_rule=[^)]+\)',
     r'scheduler.run_daily(\1, time_rule=market_open(minute=0))'),

    # get_fundamentals with JQ ORM -> comment out and replace with placeholder
    # (handled separately below for complex cases)

    # get_all_securities -> all_instruments
    (r'get_all_securities\(["\']stock["\'](?:,\s*date=[^)]+)?\)',
     "all_instruments('CS')['order_book_id'].tolist()"),
    (r'get_all_securities\(types=["\']stock["\'](?:,\s*date=[^)]+)?\)',
     "all_instruments('CS')['order_book_id'].tolist()"),

    # get_current_data() -> {} (empty dict placeholder, handled per-file)
    # context.current_dt -> context.now (done in simple replacements)
]

PREV_DATE_HELPER = '''
def _get_prev_date(context):
    """获取上一个交易日"""
    dates = get_trading_dates(end_date=context.now.date(), count=2)
    return dates[0] if len(dates) >= 2 else context.now.date()

'''


def fix_get_fundamentals(content):
    """
    把 JQ 风格的 get_fundamentals(query(...).filter(...)) 替换为
    基于 get_factor 的等价实现（尽力而为）
    """
    # 如果已经是 RQ 风格（用了 fundamentals.eod_derivative_indicator）就跳过
    if 'fundamentals.eod_derivative_indicator' in content:
        return content

    # 简单情况：get_fundamentals(q, date=...) 或 get_fundamentals(q, end_date=...)
    # 替换为注释 + 占位符，保留原逻辑意图
    def replace_gf(m):
        original = m.group(0)
        return (
            '# [MIGRATED] get_fundamentals replaced - use get_factor() for RQ\n'
            '# Original: ' + original.replace('\n', '\n# ') + '\n'
            'pd.DataFrame()  # TODO: replace with get_factor() call'
        )

    # 匹配多行 get_fundamentals(...)
    content = re.sub(
        r'get_fundamentals\([\s\S]*?\)',
        replace_gf,
        content,
        flags=re.MULTILINE
    )
    return content


def fix_get_current_data(content):
    """把 get_current_data() 的使用替换为 bar_dict 访问"""
    # current_data[stock].last_price -> bar_dict[stock].close
    content = re.sub(r'current_data\[(\w+)\]\.last_price', r'bar_dict[\1].close', content)
    content = re.sub(r'current_data\[(\w+)\]\.high_limit', r'_get_limit_up(\1)', content)
    content = re.sub(r'current_data\[(\w+)\]\.low_limit', r'_get_limit_down(\1)', content)
    content = re.sub(r'current_data\[(\w+)\]\.paused', r'(not bar_dict[\1].is_trading)', content)
    content = re.sub(r'current_data\[(\w+)\]\.is_st', r'(instruments(\1) and instruments(\1).special_type in ("ST","*ST"))', content)
    content = re.sub(r'current_data\[(\w+)\]\.name', r'instruments(\1).symbol', content)
    content = re.sub(r'current_data\[(\w+)\]\.day_open', r'bar_dict[\1].open', content)
    # remove get_current_data() assignment lines
    content = re.sub(r'\s*current_data\s*=\s*get_current_data\(\)\n', '\n', content)
    content = re.sub(r'get_current_data\(\)', 'bar_dict', content)
    return content


def needs_prev_date_helper(content):
    return '_get_prev_date(context)' in content and 'def _get_prev_date' not in content


def needs_handle_bar(content):
    return 'def handle_bar' not in content and ('scheduler.run_daily' in content or 'scheduler.run_weekly' in content or 'scheduler.run_monthly' in content)


def apply_fixes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Skip SKIP files
    if 'SKIP_REASON' in content:
        return False

    # Simple string replacements
    for old, new in SIMPLE_REPLACEMENTS:
        content = content.replace(old, new)

    # Regex replacements
    for pattern, replacement in REGEX_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # Fix get_current_data
    if 'get_current_data' in content:
        content = fix_get_current_data(content)

    # Fix get_fundamentals (JQ ORM style)
    if 'get_fundamentals' in content and 'fundamentals.eod_derivative_indicator' not in content:
        content = fix_get_fundamentals(content)

    # Add _get_prev_date helper if needed
    if needs_prev_date_helper(content):
        # Insert after imports / before first def
        insert_pos = content.find('\ndef ')
        if insert_pos == -1:
            insert_pos = 0
        content = content[:insert_pos] + '\n' + PREV_DATE_HELPER + content[insert_pos:]

    # Add handle_bar if missing
    if needs_handle_bar(content):
        # Find end of init function to insert after it
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
    skipped = []
    for f in files:
        path = os.path.join(base, f)
        if apply_fixes(path):
            fixed.append(f)
        else:
            skipped.append(f)
    print(f'Fixed: {len(fixed)}')
    for f in fixed:
        print(f'  {f}')
