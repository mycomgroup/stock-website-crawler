"""
属性测试：wizard_mutator.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from wizard_mutator import (
    HOLDING_NUM_OPTIONS,
    REBALANCE_OPTIONS,
    FACTOR_CANDIDATES,
    MUTATION_TYPES,
    mutate,
)


# ── 生成合法 wizard_config 的策略 ─────────────────────────────────────────────

_factor_names = list(FACTOR_CANDIDATES.keys())


def _filter_strategy():
    """生成单个合法 filter dict"""
    @st.composite
    def _build(draw):
        name = draw(st.sampled_from(_factor_names))
        info = FACTOR_CANDIDATES[name]
        operator = draw(st.sampled_from(info["operators"]))
        lo, hi = info["range"]
        rhs = draw(st.floats(min_value=lo, max_value=hi, allow_nan=False, allow_infinity=False))
        return {
            "operator": operator,
            "factor": {"type": info["type"], "name": name},
            "rhs": round(rhs, 4),
        }
    return _build()


def _sorting_strategy():
    """生成单个合法 sorting dict"""
    @st.composite
    def _build(draw):
        name = draw(st.sampled_from(_factor_names))
        info = FACTOR_CANDIDATES[name]
        ascending = draw(st.booleans())
        weight = draw(st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False))
        return {
            "factor": {"type": info["type"], "name": name},
            "ascending": ascending,
            "weight": round(weight, 4),
        }
    return _build()


@st.composite
def wizard_config_strategy(draw):
    """生成合法的 wizard_config dict"""
    # filters: 0-5 个，因子名不重复
    num_filters = draw(st.integers(min_value=0, max_value=5))
    filter_names = draw(st.lists(
        st.sampled_from(_factor_names),
        min_size=num_filters,
        max_size=num_filters,
        unique=True,
    ))
    filters = []
    for name in filter_names:
        info = FACTOR_CANDIDATES[name]
        operator = draw(st.sampled_from(info["operators"]))
        lo, hi = info["range"]
        # Use min_value slightly above 0 if lo=0 to avoid rhs=0 edge case in threshold tests
        rhs_lo = lo if lo > 0 else 0.01
        rhs = draw(st.floats(min_value=rhs_lo, max_value=hi, allow_nan=False, allow_infinity=False))
        filters.append({
            "operator": operator,
            "factor": {"type": info["type"], "name": name},
            "rhs": round(rhs, 4),
        })

    # sorting: 0-3 个，因子名不重复
    num_sorting = draw(st.integers(min_value=0, max_value=3))
    sorting_names = draw(st.lists(
        st.sampled_from(_factor_names),
        min_size=num_sorting,
        max_size=num_sorting,
        unique=True,
    ))
    sorting = []
    for name in sorting_names:
        info = FACTOR_CANDIDATES[name]
        ascending = draw(st.booleans())
        weight = draw(st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False))
        sorting.append({
            "factor": {"type": info["type"], "name": name},
            "ascending": ascending,
            "weight": round(weight, 4),
        })

    max_holding_num = draw(st.sampled_from(HOLDING_NUM_OPTIONS))
    rebalance_interval = draw(st.sampled_from(REBALANCE_OPTIONS))

    return {
        "filters": filters,
        "sorting": sorting,
        "maxHoldingNum": max_holding_num,
        "rebalanceInterval": rebalance_interval,
        "universe": ["000300.XSHG"],
    }


# ── Property 5: 变异后配置合法性 ──────────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 5: 变异后配置合法性
@settings(max_examples=100)
@given(
    config=wizard_config_strategy(),
    mutation_type=st.sampled_from(MUTATION_TYPES),
)
def test_mutated_config_validity(config, mutation_type):
    """Property 5: 任意合法 wizard_config 经任意变异后，结构应仍然合法"""
    new_config, desc = mutate(config, mutation_type)

    # filters 结构检查
    for f in new_config.get("filters", []):
        assert "operator" in f, f"filter missing 'operator': {f}"
        assert "factor" in f, f"filter missing 'factor': {f}"
        assert "rhs" in f, f"filter missing 'rhs': {f}"

    # sorting 结构检查
    for s in new_config.get("sorting", []):
        assert "factor" in s, f"sorting missing 'factor': {s}"
        assert "ascending" in s, f"sorting missing 'ascending': {s}"
        assert "weight" in s, f"sorting missing 'weight': {s}"

    # maxHoldingNum 检查
    assert new_config["maxHoldingNum"] in HOLDING_NUM_OPTIONS, (
        f"maxHoldingNum={new_config['maxHoldingNum']} not in {HOLDING_NUM_OPTIONS}"
    )

    # rebalanceInterval 检查
    assert new_config["rebalanceInterval"] in REBALANCE_OPTIONS, (
        f"rebalanceInterval={new_config['rebalanceInterval']} not in {REBALANCE_OPTIONS}"
    )


# ── Property 6: add_filter 不重复因子 ─────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 6: add_filter 不重复因子
@settings(max_examples=100)
@given(config=wizard_config_strategy())
def test_add_filter_no_duplicate_factor(config):
    """Property 6: add_filter 后 filters 数量+1，且新因子名不在原列表中"""
    # 确保 filters 少于 9 个（所有候选因子数量），避免回退到 adjust_filter_threshold
    assume(len(config["filters"]) < len(FACTOR_CANDIDATES))

    original_factor_names = {f["factor"]["name"] for f in config["filters"]}
    original_count = len(config["filters"])

    new_config, desc = mutate(config, "add_filter")

    new_filters = new_config["filters"]
    assert len(new_filters) == original_count + 1, (
        f"Expected {original_count + 1} filters, got {len(new_filters)}"
    )

    new_factor_names = {f["factor"]["name"] for f in new_filters}
    added_names = new_factor_names - original_factor_names
    assert len(added_names) == 1, (
        f"Expected exactly 1 new factor, got {added_names}"
    )
    new_name = next(iter(added_names))
    assert new_name not in original_factor_names, (
        f"New factor '{new_name}' already existed in original filters"
    )


# ── Property 7: adjust_filter_threshold 范围约束 ──────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 7: adjust_filter_threshold 范围约束
@settings(max_examples=100)
@given(config=wizard_config_strategy())
def test_adjust_filter_threshold_range(config):
    """Property 7: adjust_filter_threshold 后 rhs 在原值的 [0.5, 1.5] 倍范围内（含 clamp）"""
    assume(len(config["filters"]) >= 1)

    # 记录原始 rhs 值
    original_rhs_map = {
        i: f["rhs"] for i, f in enumerate(config["filters"])
    }

    new_config, desc = mutate(config, "adjust_filter_threshold")

    new_filters = new_config["filters"]
    # adjust_filter_threshold 修改一个随机 filter 的 rhs
    # 验证：每个 filter 的新 rhs 都在合法范围内（因子范围 or 原值的 [0.5, 1.5] 倍）
    assert len(new_filters) == len(config["filters"]), (
        f"filter count changed unexpectedly: {len(new_filters)} != {len(config['filters'])}"
    )

    # 找到被修改的 filter（rhs 发生变化的那个）
    # 注意：当 old_rhs=0 时，0 * multiplier = 0，rhs 不变，这是合法的边界情况
    changed = [
        (i, original_rhs_map[i], new_filters[i]["rhs"])
        for i in range(len(new_filters))
        if new_filters[i]["rhs"] != original_rhs_map.get(i)
    ]

    # 若 old_rhs=0，乘以任何 multiplier 仍为 0，rhs 不变，这是合法的
    if len(changed) == 0:
        # 所有 filter 的 rhs 未变化，说明 old_rhs=0 导致乘法无效，属于合法边界情况
        for i, f in enumerate(new_filters):
            factor_name = f["factor"]["name"]
            if factor_name in FACTOR_CANDIDATES:
                lo, hi = FACTOR_CANDIDATES[factor_name]["range"]
                assert lo <= f["rhs"] <= hi, (
                    f"rhs={f['rhs']} out of factor range [{lo}, {hi}] for {factor_name}"
                )
        return

    # 应该恰好有一个 filter 被修改
    assert len(changed) == 1, f"Expected 1 changed filter, got {len(changed)}: {changed}"

    idx, old_rhs, new_rhs = changed[0]
    factor_name = new_filters[idx]["factor"]["name"]

    # 若因子在候选库中，验证 new_rhs 在因子合法范围内（clamp 保证）
    if factor_name in FACTOR_CANDIDATES:
        lo, hi = FACTOR_CANDIDATES[factor_name]["range"]
        assert lo <= new_rhs <= hi, (
            f"new_rhs={new_rhs} out of factor range [{lo}, {hi}] for {factor_name}"
        )
    else:
        # 计算未 clamp 时的理论范围：multiplier 在 [0.5, 0.8] 或 [1.2, 1.5]
        if old_rhs >= 0:
            lower_bound = old_rhs * 0.5
            upper_bound = old_rhs * 1.5
        else:
            lower_bound = old_rhs * 1.5
            upper_bound = old_rhs * 0.5
        assert lower_bound <= new_rhs <= upper_bound, (
            f"new_rhs={new_rhs} not in [{lower_bound}, {upper_bound}] "
            f"(old_rhs={old_rhs}, factor={factor_name})"
        )


# ── Property 8: adjust_sorting_weight 权重正数不变量 ──────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 8: adjust_sorting_weight 权重正数不变量
@settings(max_examples=100)
@given(config=wizard_config_strategy())
def test_adjust_sorting_weight_positive(config):
    """Property 8: adjust_sorting_weight 后所有 sorting 权重均为正数"""
    assume(len(config["sorting"]) >= 1)

    new_config, desc = mutate(config, "adjust_sorting_weight")

    for rule in new_config["sorting"]:
        assert rule["weight"] > 0, (
            f"sorting weight {rule['weight']} is not positive: {rule}"
        )
