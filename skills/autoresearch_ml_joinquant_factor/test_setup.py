#!/usr/bin/env python3
"""测试修改后的 setup.py 功能"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from setup import _load_all_factors, prescreen_factors_simple

def test_factor_loading():
    """测试因子加载功能"""
    print("测试因子加载...")
    all_factors = _load_all_factors()
    print(f"加载的因子数量: {len(all_factors)}")
    
    # 检查是否有重复
    unique_factors = set(all_factors)
    print(f"唯一因子数量: {len(unique_factors)}")
    
    if len(all_factors) != len(unique_factors):
        print("警告: 发现重复因子!")
    else:
        print("✓ 因子加载正常")
    
    return all_factors

def test_prescreening(all_factors):
    """测试因子预筛选功能"""
    print("\n测试因子预筛选...")
    
    # 测试筛选到120个因子
    target_count = 120
    screened_factors = prescreen_factors_simple(all_factors, target_count=target_count)
    
    print(f"原始因子数量: {len(all_factors)}")
    print(f"筛选后因子数量: {len(screened_factors)}")
    print(f"目标数量: {target_count}")
    
    if len(screened_factors) == target_count:
        print("✓ 预筛选功能正常")
    else:
        print(f"警告: 筛选后数量 {len(screened_factors)} 不等于目标数量 {target_count}")
    
    # 检查是否有重复
    unique_screened = set(screened_factors)
    if len(screened_factors) != len(unique_screened):
        print("警告: 筛选后的因子有重复!")
    else:
        print("✓ 筛选后的因子无重复")
    
    # 检查是否所有筛选后的因子都在原始因子中
    missing = [f for f in screened_factors if f not in all_factors]
    if missing:
        print(f"警告: {len(missing)} 个筛选后的因子不在原始因子列表中")
    else:
        print("✓ 所有筛选后的因子都在原始因子列表中")
    
    return screened_factors

def test_diversity(screened_factors):
    """测试多样性"""
    print("\n测试因子多样性...")
    
    from factor_categories import FACTOR_TO_CATEGORY, calculate_diversity_score
    
    # 计算多样性得分（原始方法）
    diversity = calculate_diversity_score(screened_factors)
    print(f"多样性得分（原始）: {diversity:.3f}")
    
    # 分析类别分布
    category_counts = {}
    for factor in screened_factors:
        category = FACTOR_TO_CATEGORY.get(factor, "unknown")
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("类别分布:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 个因子")
    
    # 计算类别覆盖率
    total_categories = len(set(FACTOR_TO_CATEGORY.values()))
    covered_categories = len(category_counts)
    category_coverage = covered_categories / total_categories
    
    print(f"类别覆盖率: {covered_categories}/{total_categories} = {category_coverage:.1%}")
    
    # 计算类别均匀度（熵）
    import math
    total_factors = len(screened_factors)
    entropy = 0.0
    for count in category_counts.values():
        p = count / total_factors
        if p > 0:
            entropy -= p * math.log(p)
    
    max_entropy = math.log(len(category_counts)) if len(category_counts) > 0 else 0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    print(f"类别均匀度（熵）: {normalized_entropy:.3f}")
    
    # 评估标准
    if category_coverage >= 0.8 and normalized_entropy >= 0.6:
        print("✓ 多样性良好")
    elif category_coverage >= 0.6 and normalized_entropy >= 0.4:
        print("✓ 多样性中等")
    else:
        print("警告: 多样性需要改进")

def main():
    print("=" * 60)
    print("测试 setup.py 因子预筛选功能")
    print("=" * 60)
    
    # 测试因子加载
    all_factors = test_factor_loading()
    
    # 测试预筛选
    screened_factors = test_prescreening(all_factors)
    
    # 测试多样性
    test_diversity(screened_factors)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()