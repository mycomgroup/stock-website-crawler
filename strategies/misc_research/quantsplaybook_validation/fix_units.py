"""
Fix unit issues in get_factor filters:
- market_cap in RQ get_factor is in 亿元 (100M RMB), not yuan
  So 10亿 = 10, 100亿 = 100, 1000亿 = 1000
- net_profit_margin, gross_profit_margin, inc_net_profit_year_on_year, or_yoy
  are in percentage (5.0 = 5%), not decimal (0.05)
- dividend_yield is in percentage (2.0 = 2%), not decimal (0.02)
"""
import os

BASE = 'strategies/quantsplaybook_validation/strategies'

# market_cap replacements: yuan -> 亿元
# 1亿 = 100000000, so divide by 1e8
MARKET_CAP_FIXES = [
    # (wrong_value, correct_value_in_yi)
    ('> 1000000000',  '> 10'),      # > 10亿
    ('< 1000000000',  '< 10'),
    ('> 10000000000', '> 100'),     # > 100亿
    ('< 10000000000', '< 100'),
    ('> 100000000000','> 1000'),    # > 1000亿
    ('< 100000000000','< 1000'),
    ('> 500000000',   '> 5'),       # > 5亿
    ('< 500000000',   '< 5'),
    ('> 2000000000',  '> 20'),      # > 20亿
    ('< 2000000000',  '< 20'),
    ('> 3000000000',  '> 30'),
    ('< 3000000000',  '< 30'),
    ('> 5000000000',  '> 50'),
    ('< 5000000000',  '< 50'),
    ('> 200000000000','> 2000'),
    ('< 200000000000','< 2000'),
    ('> 50000000000', '> 500'),
    ('< 50000000000', '< 500'),
    ('> 30000000000', '> 300'),
    ('< 30000000000', '< 300'),
    ('> 20000000000', '> 200'),
    ('< 20000000000', '< 200'),
    ('> 15000000000', '> 150'),
    ('< 15000000000', '< 150'),
    ('> 8000000000',  '> 80'),
    ('< 8000000000',  '< 80'),
    ('> 6000000000',  '> 60'),
    ('< 6000000000',  '< 60'),
    ('> 4000000000',  '> 40'),
    ('< 4000000000',  '< 40'),
    ('> 1500000000',  '> 15'),
    ('< 1500000000',  '< 15'),
    ('> 800000000',   '> 8'),
    ('< 800000000',   '< 8'),
    ('> 300000000',   '> 3'),
    ('< 300000000',   '< 3'),
    ('> 100000000',   '> 1'),
    ('< 100000000',   '< 1'),
    ('== 0',          '== 0'),  # keep as is
    ('> 0',           '> 0'),   # keep as is
]

# percentage factor fixes: decimal -> percentage
# net_profit_margin, gross_profit_margin, inc_net_profit_year_on_year, or_yoy, dividend_yield
PCT_FACTORS = [
    'net_profit_margin',
    'gross_profit_margin', 
    'inc_net_profit_year_on_year',
    'or_yoy',
    'net_profit_yoy',
    'dividend_yield',
    'operating_profit_margin',
]

PCT_FIXES = [
    ('> 0.02',  '> 2'),
    ('> 0.03',  '> 3'),
    ('> 0.05',  '> 5'),
    ('> 0.08',  '> 8'),
    ('> 0.10',  '> 10'),
    ('> 0.1',   '> 10'),
    ('> 0.15',  '> 15'),
    ('> 0.20',  '> 20'),
    ('> 0.2',   '> 20'),
    ('> 0.25',  '> 25'),
    ('> 0.30',  '> 30'),
    ('> 0.3',   '> 30'),
    ('> 0.50',  '> 50'),
    ('> 0.5',   '> 50'),
    ('< 0.02',  '< 2'),
    ('< 0.05',  '< 5'),
    ('< 0.10',  '< 10'),
    ('< 0.1',   '< 10'),
    ('< 0.20',  '< 20'),
    ('< 0.2',   '< 20'),
    ('> 0.0',   '> 0'),
    ('< 0.0',   '< 0'),
    ('>= 0.02', '>= 2'),
    ('>= 0.05', '>= 5'),
]

files = sorted([f for f in os.listdir(BASE) if f.endswith('.py')])
fixed_files = []

for fname in files:
    path = os.path.join(BASE, fname)
    lines = open(path).readlines()
    new_lines = []
    changed = False

    for line in lines:
        new_line = line
        stripped = line.lstrip()
        if stripped.startswith('#'):
            new_lines.append(line)
            continue

        # Fix market_cap filters
        if 'market_cap' in line:
            for wrong, correct in MARKET_CAP_FIXES:
                if wrong in line and correct != wrong:
                    # Only fix if it's in a filter context
                    if "df[df['market_cap']" in line or "df['market_cap']" in line or "latest['market_cap']" in line:
                        new_line = new_line.replace(wrong, correct)
                        if new_line != line:
                            changed = True

        # Fix percentage factor filters
        for factor in PCT_FACTORS:
            if factor in new_line:
                for wrong, correct in PCT_FIXES:
                    if wrong in new_line and correct != wrong:
                        # Only fix if it's in a filter/comparison context
                        if f"['{factor}']" in new_line or f'["{factor}"]' in new_line:
                            new_line = new_line.replace(wrong, correct)
                            if new_line != line:
                                changed = True

        new_lines.append(new_line)

    if changed:
        open(path, 'w').writelines(new_lines)
        fixed_files.append(fname)

print(f'Fixed unit issues in {len(fixed_files)} files:')
for f in fixed_files:
    print(f'  {f}')
