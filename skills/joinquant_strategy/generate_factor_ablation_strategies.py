#!/usr/bin/env python3
"""
RFScore7因子消融测试策略生成器
基于 rfscore7_pb10_final.py 生成各种变体用于对比回测
"""

import os
import re

BASE_FILE = '/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore_offensive/rfscore7_pb10_final.py'
OUTPUT_DIR = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/ablation_strategies'

FACTORS = ['ROA', 'DELTA_ROA', 'OCFOA', 'ACCRUAL', 'DELTA_LEVELER', 'DELTA_MARGIN', 'DELTA_TURN']

def read_base_code():
    with open(BASE_FILE, 'r') as f:
        return f.read()

def generate_ablation_code(base_code, exclude_factor):
    """
    生成去掉某个因子的版本
    """
    code = base_code
    
    # 修改文件头部注释
    header_pattern = r'^(#.*?\n)'
    new_header = f"# RFScore7 因子消融测试 - 去除 {exclude_factor}\n# 基于 rfscore7_pb10_final.py\n\n"
    code = new_header + code[len(re.match(header_pattern, code).group(0)):]
    
    # 在calc函数中，修改indicator_tuple
    # 找到indicator_tuple的定义并修改
    indicator_tuple_pattern = r'indicator_tuple = \(\s*roa,\s*delta_roa,\s*ocfoa,\s*accrual,\s*delta_leveler,\s*delta_margin,\s*delta_turn,\s*\)'
    
    factor_map = {
        'ROA': 'roa',
        'DELTA_ROA': 'delta_roa',
        'OCFOA': 'ocfoa',
        'ACCRUAL': 'accrual',
        'DELTA_LEVELER': 'delta_leveler',
        'DELTA_MARGIN': 'delta_margin',
        'DELTA_TURN': 'delta_turn'
    }
    
    exclude_var = factor_map[exclude_factor]
    
    # 构建新的indicator_tuple
    all_vars = ['roa', 'delta_roa', 'ocfoa', 'accrual', 'delta_leveler', 'delta_margin', 'delta_turn']
    remaining_vars = [v for v in all_vars if v != exclude_var]
    new_tuple = 'indicator_tuple = (\n            ' + ',\n            '.join(remaining_vars) + ',\n        )'
    
    code = re.sub(indicator_tuple_pattern, new_tuple, code, flags=re.MULTILINE)
    
    # 修改columns
    columns_pattern = r'self\.basic\.columns = \[\s*"ROA",\s*"DELTA_ROA",\s*"OCFOA",\s*"ACCRUAL",\s*"DELTA_LEVELER",\s*"DELTA_MARGIN",\s*"DELTA_TURN",\s*\]'
    remaining_cols = [f for f in FACTORS if f != exclude_factor]
    new_columns = 'self.basic.columns = [\n            "' + '",\n            "'.join(remaining_cols) + '",\n        ]'
    code = re.sub(columns_pattern, new_columns, code, flags=re.MULTILINE)
    
    # 修改fscore计算 - 改为6因子
    fscore_pattern = r'self\.fscore = self\.basic\.apply\(sign\)\.sum\(axis=1\)'
    code = re.sub(fscore_pattern, f'self.fscore = self.basic.apply(sign).sum(axis=1)  # 6 factors (removed {exclude_factor})', code)
    
    # 修改选股逻辑 - RFScore=7改为RFScore=6
    primary_pattern = r'\(df\["RFScore"\] == 7\)'
    code = re.sub(primary_pattern, '(df["RFScore"] >= 6)', code)
    
    return code

def generate_pb_only_code(base_code):
    """
    生成只用PB筛选的版本（去掉所有RFScore因子）
    """
    code = base_code
    
    new_header = "# 纯PB筛选测试 - 无RFScore因子\n# 用于验证PB本身对收益的贡献\n\n"
    
    # 找到calc函数的位置，简化它
    calc_pattern = r'(class RFScore\(Factor\):.*?def calc\(self, data\):.*?self\.fscore = .*?\n)'
    
    simplified_calc = '''class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = []

    def calc(self, data):
        # 不计算任何因子，直接返回空
        self.basic = pd.DataFrame()
        self.fscore = pd.Series(dtype=float)
'''
    
    code = new_header + re.sub(calc_pattern, simplified_calc, code, flags=re.DOTALL)
    
    # 修改选股逻辑 - 完全基于PB
    choose_pattern = r'def choose_stocks\(watch_date, hold_num\):.*?return picks\[:hold_num\], df'
    
    simplified_choose = '''def choose_stocks(watch_date, hold_num):
    """纯PB筛选，不使用RFScore"""
    stocks = get_universe(watch_date)
    
    val = get_valuation(stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    
    df = val.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["pb_ratio"])
    df["pb_group"] = pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1
    
    # 只按PB分组筛选，不使用RFScore
    primary = df[df["pb_group"] <= g.primary_pb_group].copy()
    primary = primary.sort_values("pb_ratio", ascending=True)
    picks = primary.index.tolist()
    
    if len(picks) < hold_num:
        secondary = df[df["pb_group"] <= g.reduced_pb_group].copy()
        secondary = secondary.sort_values("pb_ratio", ascending=True)
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    
    if len(picks) < hold_num:
        fallback = df.sort_values("pb_ratio", ascending=True)
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    
    return picks[:hold_num], df'''
    
    code = re.sub(choose_pattern, simplified_choose, code, flags=re.DOTALL)
    
    return code

def generate_single_factor_code(base_code, factor_name):
    """
    生成只用单个因子的版本
    """
    factor_impl = {
        'ROA': '''        roa = data["roa"]
        self.basic = pd.DataFrame({"ROA": roa})
        self.fscore = (roa > 0).astype(int)''',
        
        'DELTA_ROA': '''        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1
        self.basic = pd.DataFrame({"DELTA_ROA": delta_roa})
        self.fscore = (delta_roa > 0).astype(int)''',
        
        'OCFOA': '''        cfo_sum = (data["net_operate_cash_flow"] + data["net_operate_cash_flow_1"] + 
                   data["net_operate_cash_flow_2"] + data["net_operate_cash_flow_3"])
        ta_ttm = (data["total_assets"] + data["total_assets_1"] + 
                  data["total_assets_2"] + data["total_assets_3"]) / 4
        ocfoa = cfo_sum / ta_ttm
        self.basic = pd.DataFrame({"OCFOA": ocfoa})
        self.fscore = (ocfoa > 0).astype(int)''',
        
        'ACCRUAL': '''        cfo_sum = (data["net_operate_cash_flow"] + data["net_operate_cash_flow_1"] + 
                   data["net_operate_cash_flow_2"] + data["net_operate_cash_flow_3"])
        ta_ttm = (data["total_assets"] + data["total_assets_1"] + 
                  data["total_assets_2"] + data["total_assets_3"]) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - data["roa"] * 0.01
        self.basic = pd.DataFrame({"ACCRUAL": accrual})
        self.fscore = (accrual > 0).astype(int)''',
        
        'DELTA_LEVELER': '''        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)
        self.basic = pd.DataFrame({"DELTA_LEVELER": delta_leveler})
        self.fscore = (delta_leveler > 0).astype(int)''',
        
        'DELTA_MARGIN': '''        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1
        self.basic = pd.DataFrame({"DELTA_MARGIN": delta_margin})
        self.fscore = (delta_margin > 0).astype(int)''',
        
        'DELTA_TURN': '''        turnover = data["operating_revenue"] / (data["total_assets"] + data["total_assets_1"]).mean()
        turnover_1 = data["operating_revenue_4"] / (data["total_assets_4"] + data["total_assets_5"]).mean()
        delta_turn = turnover / turnover_1 - 1
        self.basic = pd.DataFrame({"DELTA_TURN": delta_turn})
        self.fscore = (delta_turn > 0).astype(int)'''
    }
    
    code = base_code
    
    new_header = f"# 单因子测试 - 只用 {factor_name}\n# 用于验证单个因子的贡献\n\n"
    
    calc_pattern = r'(def calc\(self, data\):.*?self\.fscore = .*?\n)'
    
    new_calc = f'''    def calc(self, data):
        {factor_impl[factor_name]}'''
    
    code = new_header + re.sub(calc_pattern, new_calc, code, flags=re.DOTALL)
    
    # 修改选股逻辑 - 改为score=1（因为单因子最高只有1分）
    primary_pattern = r'\(df\["RFScore"\] == 7\)'
    code = re.sub(primary_pattern, '(df["RFScore"] == 1)', code)
    
    secondary_pattern = r'\(df\["RFScore"\] >= 6\)'
    code = re.sub(secondary_pattern, '(df["RFScore"] == 1)', code)
    
    return code

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    base_code = read_base_code()
    
    # 生成基线版本（完整版）
    baseline_code = base_code.replace('from jqdata import *', '# RFScore7 基线版本 - 完整7因子\nfrom jqdata import *')
    with open(os.path.join(OUTPUT_DIR, 'baseline_full7.py'), 'w') as f:
        f.write(baseline_code)
    print('Generated: baseline_full7.py')
    
    # 生成消融版本（去掉每个因子）
    for factor in FACTORS:
        ablation_code = generate_ablation_code(base_code, factor)
        filename = f'ablation_no_{factor.lower()}.py'
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            f.write(ablation_code)
        print(f'Generated: {filename}')
    
    # 生成纯PB版本
    pb_only_code = generate_pb_only_code(base_code)
    with open(os.path.join(OUTPUT_DIR, 'pb_only_no_rfscore.py'), 'w') as f:
        f.write(pb_only_code)
    print('Generated: pb_only_no_rfscore.py')
    
    # 生成单因子版本
    for factor in FACTORS:
        single_factor_code = generate_single_factor_code(base_code, factor)
        filename = f'single_factor_{factor.lower()}.py'
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            f.write(single_factor_code)
        print(f'Generated: {filename}')
    
    print(f'\nAll variants generated in: {OUTPUT_DIR}')
    print(f'Total: 1 baseline + 7 ablation + 1 pb_only + 7 single_factor = 16 variants')

if __name__ == '__main__':
    main()