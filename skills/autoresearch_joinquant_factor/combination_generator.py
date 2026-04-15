#!/usr/bin/env python
# coding: utf-8
"""
因子组合生成器
支持三种策略：
1. 随机采样
2. 频率优先（基于已有高分组合统计）
3. 高分组合变异
"""

import random
import numpy as np
from typing import List, Set, Tuple, Optional
from collections import Counter


def _get_factor_category(factor: str) -> str:
    """获取因子所属类别"""
    from factor_categories import FACTOR_CATEGORIES
    for cat, fs in FACTOR_CATEGORIES.items():
        if factor in fs:
            return cat
    return "unknown"


class CombinationGenerator:
    def __init__(
        self,
        factor_pool: List[str],
        existing_combinations: List[List[str]],
        tried_combinations: Optional[Set[Tuple[str, ...]]] = None,
    ):
        self.factor_pool = factor_pool
        self.existing_combinations = existing_combinations
        self.tried_combinations = tried_combinations or set()

        # 统计因子频率
        self.factor_frequency = self._calculate_frequency()

        # 记录当前最优组合
        self.best_combinations = []

        # 阶段控制
        self.iteration_count = 0
        self.phase = "explore"  # explore 或 converge

    def _calculate_frequency(self) -> Counter:
        """统计已有高分组合中各因子的出现频率"""
        all_factors = []
        for combo in self.existing_combinations:
            all_factors.extend(combo)
        return Counter(all_factors)

    def _is_tried(self, combination: List[str]) -> bool:
        """检查组合是否已尝试过"""
        key = tuple(sorted(combination))
        return key in self.tried_combinations

    def _mark_tried(self, combination: List[str]):
        """标记组合为已尝试"""
        key = tuple(sorted(combination))
        self.tried_combinations.add(key)

    def _calculate_diversity(self, combo: List[str]) -> float:
        """计算组合的多样性分数"""
        if len(combo) <= 1:
            return 1.0
        categories = [_get_factor_category(f) for f in combo]
        unique = len(set(categories))
        return unique / len(combo)

    def generate_random(self, size: Optional[int] = None) -> List[str]:
        """随机采样策略（优先高多样性）"""
        if size is None:
            size = random.randint(2, 5)

        max_attempts = 200  # 增加尝试次数以寻找高多样性组合
        best_combo = None
        best_diversity = 0

        for _ in range(max_attempts):
            combo = random.sample(self.factor_pool, size)
            if not self._is_tried(combo):
                diversity = self._calculate_diversity(combo)
                # 优先选择多样性 >= 0.5 的组合
                if diversity >= 0.5:
                    return combo
                # 记录最高多样性组合作为后备
                if diversity > best_diversity:
                    best_diversity = diversity
                    best_combo = combo

        # 如果没有找到足够多样性的组合，返回最好的一个
        return best_combo if best_combo else None

    def generate_frequency_based(self, size: Optional[int] = None) -> List[str]:
        """频率优先策略（优先高多样性）"""
        if size is None:
            size = random.randint(2, 5)

        # 构建权重列表
        factors = list(self.factor_pool)
        weights = np.array(
            [self.factor_frequency.get(f, 0) + 1 for f in factors], dtype=float
        )

        # 归一化并增加高频因子权重
        weights = weights**2  # 平方放大差异
        weights = weights / weights.sum()

        max_attempts = 200  # 增加尝试次数
        best_combo = None
        best_diversity = 0

        for _ in range(max_attempts):
            try:
                combo = np.random.choice(factors, size=size, replace=False, p=weights)
                combo = combo.tolist()
                if not self._is_tried(combo):
                    diversity = self._calculate_diversity(combo)
                    # 优先选择多样性 >= 0.5 的组合
                    if diversity >= 0.5:
                        return combo
                    # 记录最高多样性组合作为后备
                    if diversity > best_diversity:
                        best_diversity = diversity
                        best_combo = combo
            except:
                # 如果采样失败，回退到随机
                return self.generate_random(size)

        return best_combo if best_combo else self.generate_random(size)

    def generate_mutation(
        self, base_combo: List[str], num_mutations: int = 1
    ) -> List[str]:
        """高分组合变异策略"""
        pool_set = set(self.factor_pool)
        base_set = set(base_combo)

        # 可替换的因子（在因子池中但不在当前组合中）
        available = list(pool_set - base_set)

        if not available:
            return None

        max_attempts = 100
        for _ in range(max_attempts):
            new_combo = base_combo.copy()

            # 随机替换 1-2 个因子
            num_replace = min(num_mutations, len(base_combo))
            replace_indices = random.sample(range(len(base_combo)), num_replace)

            for idx in replace_indices:
                if available:
                    new_factor = random.choice(available)
                    new_combo[idx] = new_factor
                    available.remove(new_factor)

            if not self._is_tried(new_combo):
                return new_combo
        return None

    def generate(self, phase: Optional[str] = None) -> Tuple[List[str], str]:
        """
        生成候选组合

        Returns:
            (combination, strategy_used)
        """
        self.iteration_count += 1

        if phase is None:
            phase = self.phase

        if phase == "explore":
            # 探索期：50% 随机 + 50% 频率优先
            if random.random() < 0.5:
                combo = self.generate_random()
                strategy = "random"
            else:
                combo = self.generate_frequency_based()
                strategy = "frequency"
        else:
            # 收敛期：70% 变异 + 30% 随机
            if self.best_combinations and random.random() < 0.7:
                base = random.choice(self.best_combinations)
                combo = self.generate_mutation(base)
                strategy = "mutation"
            else:
                combo = self.generate_random()
                strategy = "random"

        if combo:
            self._mark_tried(combo)

        return combo, strategy

    def update_best(self, combination: List[str], score: float, threshold: float = 1.5):
        """更新最优组合列表"""
        if score > threshold:
            self.best_combinations.append(combination)
            if score > 2.0:
                self.phase = "converge"

    def get_stats(self) -> dict:
        """获取生成器统计信息"""
        return {
            "iteration": self.iteration_count,
            "phase": self.phase,
            "tried_count": len(self.tried_combinations),
            "best_count": len(self.best_combinations),
            "top_factors": self.factor_frequency.most_common(10),
        }
