# rule_library

YAML 驱动的量化选股规则库。

## 设计理念

- **配置即代码**：所有策略、排雷、搜索空间都在 YAML 里定义。外部项目（10jqka_backtest 等）只需生成符合 schema 的 YAML，就能直接跑。
- **零硬依赖**：除了 `pandas / numpy / pyyaml`，不依赖任何本仓库外的模块。
- **中文友好**：YAML 里可以直接用"EPS / ROE / 流通市值 / 营收增速"等业务名，通过 `column_aliases.yaml` 解析到真实列名；缺失的别名原样透传。
- **容错**：引用的列在数据里缺失时，跳过该规则并在诊断里记录，不会崩溃。

## 目录

```
rule_library/
├── __init__.py
├── schema.py         # Rule / Strategy / SearchSpace 数据类
├── operators.py      # 原子操作符注册表（gt/lt/between/top_pct...）
├── engine.py         # 规则应用引擎（单日横截面 → 选中股票）
├── backtest.py       # 面板回测 + 指标 + 评分公式
├── search.py         # SearchSpace → Strategy 列表展开
├── loader.py         # YAML → 数据结构
└── configs/
    ├── column_aliases.yaml   # 业务名 → CSV 列名
    ├── small_cap_base.yaml   # 小票池排雷层（T2 级）
    ├── candidates.yaml       # 第一批候选策略（6 条）
    └── search_space.yaml     # 网格搜索空间（~600 组合）
```

CLI 入口：`v2/rule_search.py`。

## YAML Schema

### Rule

```yaml
{op: gt, column: EPS, value: 0.5, name: 可选描述}
```

`op` 必填，指向 `operators.py` 注册表。`column` 可以是别名。其余字段全部作为 op 的参数。

支持的 op：
- `gt / ge / lt / le / eq / ne` — 标量比较
- `between` — `low / high / inclusive(both|left|right|neither)`
- `not_null / is_null`
- `top_pct / bottom_pct` — 按 `pct` 取横截面分位
- `rank_gt / rank_lt` — 按 rank 分位过滤

排序用虚拟 op `sort`（在 Strategy.sort_by 里用，不在 filter 列表里）。

### Strategy

```yaml
name: 小票·质量成长
hard_filters: [...]        # 硬排雷（通常来自 base_filters 注入）
soft_filters: [...]        # 软筛选
sort_by: {column: 近一月动量, ascending: false}
n_stocks: 30
rebalance_weeks: 1

# 可选：两阶段
stage1_top_pct: 0.10
stage1_sort: {column: 近一月动量, ascending: false}

meta: {tree: B_quality_growth, branch: B2}
```

### SearchSpace

```yaml
search:
  base_filters: []                 # 额外硬约束（与 small_cap_base 合并）
  filter_choices:                  # 每个 choice 是一个"槽"
    - name: 盈利门槛
      variants:
        - null                      # 表示跳过本槽
        - {op: gt, column: EPS, value: 0.3}
        - {op: gt, column: EPS, value: 0.5}
  sort_keys:
    - {column: 近一月动量, ascending: false}
  n_stocks_options: [30, 50]
  stage1_top_pcts: [null, 0.10]
  rebalance_weeks: 1
  max_combinations: 500
  random_seed: 42
```

展开规则：对所有 `filter_choices × sort_keys × n_stocks × stage1` 做笛卡尔积，
超过 `max_combinations` 时按 `random_seed` 无放回采样。

## 使用

### 跑候选策略

```bash
python v2/rule_search.py candidates \
    --data skills/autoresearch_ml_joinquant_factor_v2/data/weekly_factors \
    --out output/rule_search/candidates.csv
```

### 网格搜索

```bash
python v2/rule_search.py grid \
    --data skills/autoresearch_ml_joinquant_factor_v2/data/weekly_factors \
    --search v2/rule_library/configs/search_space.yaml \
    --out output/rule_search/grid.csv \
    --topk 50
```

### 跑单个策略

```bash
python v2/rule_search.py single \
    --data ... \
    --strategy my_strategy.yaml
```

## 评分公式

与汇总表保持一致：

```
score = sortino·0.40 + calmar·0.25 + IR·0.15 + win_rate·0.10
      - complexity · 0.10 - position_penalty - overfit_penalty
```

硬约束：`abs(max_drawdown) > 0.35` → 直接 rollback（得分 -999）。

小票池专属调整：
- `position_penalty` 在 5-40 之间免罚（大池子持仓更分散反而稳）
- `overfit_penalty` 阈值比通用版收紧 5pp（N=1 要求胜率 ≥ 65%）

## 数据约定

面板 DataFrame 需要至少含：
- `date` — datetime
- `stock_id` — 股票代码
- `pchg` — 当期已实现收益（与回测框架一致的频率）

其他列名按 `column_aliases.yaml` 映射。

## 扩展：外部项目生成 YAML

10jqka_backtest / 其他种子库只需按上面的 Schema 产出 YAML，
例如把 67 个种子策略转成 `strategies:` 列表，就可以用本库直接回测。
不需要修改任何 Python 代码。

新的操作符只需在 `operators.py` 的 `FILTER_OPS` 注册表里加一行。
