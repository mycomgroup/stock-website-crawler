# Wizard Strategy Autoresearch - 完整使用指南

本文档提供 Wizard 策略自动优化系统的详细说明，包括配置结构、因子库、变异类型、技术架构等。

---

## 目录

1. [核心特点](#核心特点)
2. [配置结构详解](#配置结构详解)
3. [因子库完整列表](#因子库完整列表)
4. [8 种变异类型详解](#8-种变异类型详解)
5. [技术架构](#技术架构)
6. [常见问题](#常见问题)
7. [与 autoresearch 的区别](#与-autoresearch-的区别)

---

## 核心特点

- **配置驱动**：优化 `wizard_config.json` 参数，无需编写代码
- **28+ 因子库**：涵盖估值、盈利、成长、财务健康、现金流、分红等维度
- **8 种变异**：智能参数调整策略，避免无效探索
- **自动回测**：通过 HTTP API 提交回测，轮询结果
- **评分决策**：基于 Calmar、Sortino、IR 综合评分，自动 keep/rollback
- **完整留档**：每次迭代记录配置快照、回测结果、变异描述

---

## 配置结构详解

### wizard_config.json 完整示例

```json
{
  "universe": ["000300.XSHG"],
  "stOption": "exclude",
  "filters": [
    {
      "operator": "less_than",
      "factor": {"type": "fundamental", "name": "pe_ratio"},
      "rhs": 20
    },
    {
      "operator": "greater_than",
      "factor": {"type": "fundamental", "name": "dividend_yield"},
      "rhs": 2
    }
  ],
  "sorting": [
    {
      "factor": {"type": "fundamental", "name": "pb_ratio"},
      "ascending": true,
      "weight": 0.6
    },
    {
      "factor": {"type": "fundamental", "name": "roe"},
      "ascending": false,
      "weight": 0.4
    }
  ],
  "maxHoldingNum": 15,
  "rebalanceInterval": 10
}
```

### 字段详细说明

#### universe（股票池）

可选值：
- `"000300.XSHG"` - 沪深300（大盘蓝筹）
- `"000905.XSHG"` - 中证500（中盘成长）
- `"000852.XSHG"` - 中证1000（小盘）
- `"*"` - 全市场

#### stOption（ST 股票处理）

可选值：
- `"exclude"` - 排除 ST 股票（推荐）
- `"include"` - 包含 ST 股票
- `"only"` - 仅 ST 股票

#### filters（筛选条件）

每个 filter 包含：
- `operator`：操作符
  - `"greater_than"` - 大于
  - `"less_than"` - 小于
  - `"in_range"` - 在范围内
  - `"rank_in_range"` - 排名在范围内
- `factor`：因子对象
  - `type`：`"fundamental"`（基本面）或 `"pricing"`（价格）
  - `name`：因子名称（见因子库）
- `rhs`：阈值（右侧值）
  - 单值：数字
  - 范围：`[min, max]` 数组

#### sorting（排序规则）

每个 sorting 规则包含：
- `factor`：因子对象（同 filters）
- `ascending`：排序方向
  - `true` - 升序（低值优先，适合估值因子）
  - `false` - 降序（高值优先，适合盈利因子）
- `weight`：权重（正数，无需归一化）

#### maxHoldingNum（最大持仓数量）

推荐值：`5, 10, 15, 20, 25, 30`

- 值越小，持仓越集中，波动越大
- 值越大，持仓越分散，接近指数

#### rebalanceInterval（调仓间隔）

推荐值：`1, 3, 5, 10, 15, 20, 30`（单位：交易日）

- 值越小，调仓越频繁，换手率越高，摩擦成本越大
- 值越大，调仓越少，持仓更稳定

---

## 因子库完整列表

### 估值指标（Valuation）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `pe_ratio` | 市盈率 | [5, 80] | 20 | `less_than`, `in_range` |
| `pb_ratio` | 市净率 | [0.5, 5] | 2 | `less_than` |
| `ps_ratio` | 市销率 | [0.5, 10] | 3 | `less_than` |
| `pcf_ratio` | 市现率 | [5, 50] | 15 | `less_than` |
| `market_cap` | 总市值（元） | [5e8, 1e11] | 1e9 | `greater_than`, `less_than` |
| `circulating_market_cap` | 流通市值（元） | [5e8, 1e11] | 1e9 | `greater_than`, `less_than` |

### 盈利能力（Profitability）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `roe` | 净资产收益率（%） | [5, 30] | 10 | `greater_than` |
| `roa` | 总资产收益率（%） | [2, 20] | 5 | `greater_than` |
| `gross_profit_margin` | 毛利率（%） | [10, 80] | 20 | `greater_than` |
| `net_profit_margin` | 净利率（%） | [5, 50] | 10 | `greater_than` |
| `operating_profit_margin` | 营业利润率（%） | [5, 50] | 10 | `greater_than` |

### 成长能力（Growth）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `revenue_growth_rate` | 营收增长率（%） | [0, 30] | 5 | `greater_than` |
| `net_profit_growth_rate` | 净利润增长率（%） | [0, 30] | 5 | `greater_than` |
| `operating_profit_growth_rate` | 营业利润增长率（%） | [0, 30] | 5 | `greater_than` |
| `total_assets_growth_rate` | 总资产增长率（%） | [0, 30] | 5 | `greater_than` |

### 财务健康（Financial Health）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `debt_ratio` | 资产负债率（%） | [20, 70] | 50 | `less_than` |
| `current_ratio` | 流动比率 | [1, 5] | 1.5 | `greater_than` |
| `quick_ratio` | 速动比率 | [0.5, 3] | 1 | `greater_than` |
| `equity_ratio` | 产权比率 | [0.5, 3] | 1.5 | `less_than` |

### 现金流（Cash Flow）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `operating_cash_flow_per_share` | 每股经营现金流（元） | [0.5, 10] | 1 | `greater_than` |
| `free_cash_flow_per_share` | 每股自由现金流（元） | [0.5, 10] | 1 | `greater_than` |

### 分红指标（Dividend）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `dividend_yield` | 股息率（%） | [1, 8] | 2 | `greater_than` |
| `dividend_payout_ratio` | 股利支付率（%） | [20, 80] | 30 | `greater_than` |

### 每股指标（Per Share）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `eps` | 每股收益（元） | [0.5, 10] | 1 | `greater_than` |
| `book_value_per_share` | 每股净资产（元） | [5, 50] | 10 | `greater_than` |

### 价格与成交量（Pricing）

| 因子名 | 说明 | 合理范围 | 默认阈值 | 支持的 operator |
|--------|------|---------|---------|----------------|
| `turnover_rate` | 换手率（%） | [0.5, 10] | 2 | `greater_than`, `less_than` |
| `volume` | 成交量（股） | [1e6, 1e9] | 1e7 | `greater_than` |
| `change_rate` | 涨跌幅（%） | [-10, 10] | 0 | `greater_than`, `less_than` |

---

## 8 种变异类型详解

### 1. add_filter（添加筛选条件）

**描述**：新增一个筛选条件，过滤不符合要求的股票。

**示例**：
```json
{
  "operator": "greater_than",
  "factor": {"type": "fundamental", "name": "roe"},
  "rhs": 10
}
```

**适用场景**：
- 提升选股质量（如添加 `roe > 10` 过滤低质量公司）
- 降低风险（如添加 `debt_ratio < 50` 过滤高杠杆）
- 增加流动性（如添加 `turnover_rate > 2` 过滤低流动性）

### 2. remove_filter（移除筛选条件）

**描述**：删除一个现有的筛选条件，放宽选股范围。

**适用场景**：
- 选股数量过少时，放宽筛选条件
- 某个筛选条件效果不佳时，删除它

### 3. adjust_filter_threshold（调整筛选阈值）

**描述**：调整现有筛选条件的阈值（±20%~±50%）。

**示例**：
- `pe_ratio < 20` → `pe_ratio < 15`（更严格）
- `roe > 10` → `roe > 8`（更宽松）

**适用场景**：
- 微调筛选条件的严格程度
- 在保持筛选逻辑的前提下优化参数

### 4. add_sorting（添加排序规则）

**描述**：新增一个排序规则，影响持仓结构。

**示例**：
```json
{
  "factor": {"type": "fundamental", "name": "dividend_yield"},
  "ascending": false,
  "weight": 0.3
}
```

**适用场景**：
- 增加新的因子偏好（如添加高股息排序）
- 多因子组合优化

### 5. adjust_sorting_weight（调整排序权重）

**描述**：调整现有排序规则的权重（±20%~±50%）。

**示例**：
- `dividend_yield weight=0.6` → `weight=0.8`（加强高股息偏好）

**适用场景**：
- 微调因子权重，优化持仓结构

### 6. adjust_holding_num（调整持仓数量）

**描述**：调整最大持仓数量，影响集中度。

**候选值**：`5, 10, 15, 20, 25, 30`

**适用场景**：
- 集中持仓（减少持仓数量）提升收益
- 分散持仓（增加持仓数量）降低回撤

### 7. adjust_rebalance_interval（调整调仓间隔）

**描述**：调整调仓间隔，影响换手率。

**候选值**：`1, 3, 5, 10, 15, 20, 30`（单位：交易日）

**适用场景**：
- 降低换手率（增加调仓间隔）减少摩擦成本
- 提高灵活性（减少调仓间隔）快速响应市场变化

### 8. change_universe（切换股票池）

**描述**：切换股票池，变化最大，风险最高。

**候选值**：
- `000300.XSHG` - 沪深300
- `000905.XSHG` - 中证500
- `000852.XSHG` - 中证1000
- `*` - 全市场

**适用场景**：
- 当前股票池已充分优化，需要探索新空间
- 尝试不同市值风格（大盘/中盘/小盘）

---

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                         Agent                               │
│  读取 program.md → 调用 run_iteration.py     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              run_iteration.py                        │
│  1. 读取 state.json 和 wizard_config.json                  │
│  2. 调用 wizard_mutator.mutate() 生成候选配置              │
│  3. 调用 wizard_executor.submit_backtest() 提交回测        │
│  4. 轮询回测状态，获取结果                                  │
│  5. 调用 scorer.calculate_score() 计算得分                 │
│  6. 决策 keep/rollback，更新 state.json 和 iterations.tsv   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│ wizard_      │  │ wizard_executor  │  │ scorer.py    │
│ mutator.py   │  │ .py              │  │              │
│              │  │                  │  │ Calmar×0.55  │
│ 8 种变异     │  │ HTTP API 封装    │  │ Sortino×0.25 │
│ 28+ 因子库   │  │ 轮询回测状态     │  │ IR×0.20      │
└──────────────┘  └──────────────────┘  └──────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ RiceQuant API    │
                  │ 向导式策略回测   │
                  └──────────────────┘
```

---

## 常见问题

### Q1：如何添加新因子？

编辑 `wizard_mutator.py` 中的 `FACTOR_CANDIDATES` 字典，添加新因子的元数据：

```python
FACTOR_CANDIDATES = {
    "new_factor": {
        "type": "fundamental",
        "operators": ["greater_than", "less_than"],
        "range": [0, 100],
        "default": 50,
    },
    # ...
}
```

### Q2：如何调整变异策略？

修改 `wizard_mutator.py` 中的变异函数，或调整 `MUTATION_TYPES` 列表中的变异类型权重。

### Q3：如何修改评分公式？

编辑 `scorer.py` 中的 `calculate_score` 函数：

```python
def calculate_score(metrics: dict) -> float:
    calmar = metrics["calmar"]
    sortino = metrics["sortino"]
    ir = metrics["information_ratio"]
    
    # 调整权重
    score = calmar * 0.55 + sortino * 0.25 + ir * 0.20
    return score
```

### Q4：如何查看历史配置？

通过 Git 历史查看成功版本：

```bash
cd experiments/<name>
git log --oneline          # 查看所有成功版本
git show HEAD:wizard_config.json  # 查看最新配置
```

### Q5：如何手动回滚到某个历史版本？

```bash
cd experiments/<name>
git checkout <commit_hash> -- wizard_config.json
# 然后更新 state.json 中的 champion_score
```

### Q6：如何验证配置合法性？

使用 `validate.py` 工具：

```bash
python validate.py --config experiments/my_experiment/wizard_config.json
python validate.py --config experiments/my_experiment/wizard_config.json --strict
```

### Q7：如何分析实验结果？

使用 `analyze.py` 工具：

```bash
python analyze.py --base experiments/my_experiment
```

---

## 与 autoresearch 的区别

| 特性 | autoresearch_ricequant | autoresearch_ricequant-wizard |
|------|----------------------|-------------------------------|
| 优化对象 | Python 策略代码 | JSON 配置参数 |
| 策略类型 | 自定义代码策略 | RiceQuant 向导式策略 |
| 变异方式 | 代码修改（agent 自由发挥） | 8 种预定义变异类型 |
| 因子库 | 无限制（agent 可写任意代码） | 28+ 预定义因子 |
| 适用场景 | 复杂策略逻辑、自定义算法 | 快速因子选股、参数优化 |
| 学习曲线 | 需要编程能力 | 无需编程，配置即可 |
| 灵活性 | 极高（可实现任意逻辑） | 中等（受限于因子库和变异类型） |
| 稳定性 | 中等（代码可能引入 bug） | 高（配置驱动，不会语法错误） |
| 迭代速度 | 较慢（需要 agent 理解代码） | 较快（结构化变异） |

---

## 许可证

MIT

---

## 相关资源

- [README.md](./README.md) - 快速开始指南
- [program.md](./program.md) - Agent 操作指南
- [MOCK_MODE.md](./MOCK_MODE.md) - Mock 模式说明
- [autoresearch_ricequant](../autoresearch_ricequant/README.md) - 代码策略自动优化系统
- [ricequant-wizard](../ricequant-wizard/README.md) - RiceQuant 向导式策略工具集
- [RiceQuant 官方文档](https://www.ricequant.com/doc/)
