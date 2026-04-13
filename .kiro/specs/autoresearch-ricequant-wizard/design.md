# Design Document: autoresearch-ricequant-wizard

## Overview

autoresearch-ricequant-wizard 是一个针对 RiceQuant **向导式策略（Wizard Strategy）** 的自动迭代参数优化系统。与 `skills/autoresearch_ricequant/`（优化 Python 代码策略）完全独立，本系统的优化对象是 `wizard_config.json`——一个描述向导式策略参数空间的 JSON 配置文件。

系统通过调用 `skills/ricequant-wizard/run-skill.js` 的 Node.js 接口（`--update` + `--run`）来更新策略并触发回测，内置独立的评分模块，使用与 autoresearch 相同的评分公式（calmar×0.55 + sortino×0.25 + information_ratio×0.20），并通过 keep/rollback 机制维护最优配置（champion）。

### 与 autoresearch 的关键差异

| 维度 | autoresearch | autoresearch-ricequant-wizard |
|------|-------------|-------------------------------|
| 优化对象 | `strategy.py`（Python 代码） | `wizard_config.json`（JSON 参数） |
| 版本控制 | git commit/checkout | JSON 文件直接覆盖 + history 快照 |
| 平台接口 | HTTP API 直接调用 | subprocess 调用 Node.js 脚本 |
| 变异方式 | agent 手动修改代码 | Mutator 自动生成候选配置 |
| 预检查 | preflight_checker.py | 无（JSON 格式由 Mutator 保证） |

---

## Architecture

```
skills/autoresearch_ricequant-wizard/
├── scorer.py                    # 独立评分模块
├── wizard_executor.py           # 执行器：subprocess 调用 Node.js
├── wizard_mutator.py            # 变异器：8种 JSON 参数变异类型
├── run_iteration.py      # 单次迭代执行器（CLI 入口）
├── setup.py           # 初始化实验目录的辅助脚本
├── seed_wizard_config.json      # 种子配置（低估值高股息初始策略）
├── program.md            # agent 操作指南
└── experiments/
    └── <experiment_name>/
        ├── wizard_config.json   # 当前 champion 配置（可写）
        ├── state.json           # 迭代状态（只读，由脚本维护）
        └── history/
            ├── iterations.tsv
            ├── search_notes.md  # agent 维护的搜索地图
            ├── 0000_config.json # 初始配置快照
            ├── 0000.json        # 初始迭代记录
            └── ...
```

### 数据流

```
agent
  │
  ▼
run_iteration.py  ──读──▶  state.json
  │                               wizard_config.json (champion)
  │
  ├──▶ wizard_mutator.py  ──生成──▶  candidate_config (临时)
  │
  ├──▶ wizard_executor.py
  │       │
  │       ├── subprocess: node run-skill.js --update --id <id> --config <file>
  │       ├── subprocess: node run-skill.js --run --id <id> --start ... --wait
  │       │       └── 提取 backtestId（格式：回测已启动: <id>）
  │       ├── HTTP 轮询: GET /api/backtest/v1/.../backtests/<id>
  │       └── HTTP 获取: GET /api/backtest/v1/.../backtests/<id>?extra_fields=summary
  │
  ├──▶ scorer.py  ──计算──▶  score, decision
  │
  └──▶ keep/rollback
          ├── keep:     覆盖 wizard_config.json，写 history/<iter>_config.json
          └── rollback: 从 history/<champion_iter>_config.json 恢复 wizard_config.json
```

---

## Components and Interfaces

### 1. scorer.py

独立实现，与 `skills/autoresearch_ricequant/scorer.py` 逻辑相同，不依赖后者。

```python
@dataclass
class ParsedMetrics:
    status: str
    backtest_id: str
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe: float
    sortino: float
    information_ratio: float
    alpha: float
    beta: float

def parse_backtest_result(result_json: dict) -> ParsedMetrics
def calculate_score(metrics: ParsedMetrics, weights: dict = None) -> float
def decide_keep_rollback(
    new_score: float,
    champion_score: float,
    new_metrics: ParsedMetrics,
    champion_metrics: Optional[ParsedMetrics],
    hard_constraints: dict = None
) -> tuple[str, str]  # (decision, reason)
```

### 2. wizard_executor.py

路径常量：
```python
WIZARD_SKILL_DIR = Path("/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant-wizard")
SESSION_FILE = Path("/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/data/session.json")
```

核心函数：
```python
def update_strategy(strategy_id: str, config_path: str) -> None
    # subprocess: node run-skill.js --update --id <id> --config <file>
    # cwd=WIZARD_SKILL_DIR

def run_backtest(strategy_id: str, bt_config: dict) -> dict
    # subprocess: node run-skill.js --run --id <id> --start ... --wait
    # 从输出提取 backtestId（格式：回测已启动: <id>）
    # 返回 {"backtest_id": str, "status": "submitted"}

def wait_for_completion(backtest_id: str, max_wait: int, poll_interval: int) -> dict
    # 直接 HTTP 轮询（复用 ricequant_executor.py 的 session 读取和 HTTP 工具逻辑）
    # 返回 {"backtest_id": str, "status": str, "summary": dict}

def fetch_results(strategy_id: str, backtest_id: str) -> dict
    # HTTP 获取结果，映射字段到 scorer.py 期望格式
    # 返回含 annualReturn, maxDrawdown, sharpe, sortino, informationRatio 的 dict
```

异常类：
```python
class WizardExecutorError(Exception): pass
class BacktestTimeoutError(WizardExecutorError): pass
class BacktestFailedError(WizardExecutorError): pass
```

### 3. wizard_mutator.py

内嵌因子候选库：
```python
FACTOR_CANDIDATES = {
    "pe_ratio":   {"type": "fundamental", "operators": ["less_than", "in_range"], "range": [5, 80], "default_rhs": 20},
    "pb_ratio":   {"type": "fundamental", "operators": ["less_than"], "range": [0.5, 5], "default_rhs": 2},
    "roe":        {"type": "fundamental", "operators": ["greater_than"], "range": [5, 30], "default_rhs": 10},
    "dividend_yield": {"type": "fundamental", "operators": ["greater_than"], "range": [1, 8], "default_rhs": 2},
    "debt_ratio": {"type": "fundamental", "operators": ["less_than"], "range": [20, 70], "default_rhs": 50},
    "revenue_growth_rate": {"type": "fundamental", "operators": ["greater_than"], "range": [0, 30], "default_rhs": 5},
    "net_profit_growth_rate": {"type": "fundamental", "operators": ["greater_than"], "range": [0, 30], "default_rhs": 5},
    "market_cap": {"type": "fundamental", "operators": ["greater_than", "less_than"], "range": [5e8, 1e11], "default_rhs": 1e9},
    "turnover_rate": {"type": "pricing", "operators": ["greater_than", "less_than"], "range": [0.5, 10], "default_rhs": 2},
}
UNIVERSE_OPTIONS = ["000300.XSHG", "000905.XSHG", "000852.XSHG", "*"]
HOLDING_NUM_OPTIONS = [5, 10, 15, 20, 25, 30]
REBALANCE_OPTIONS = [1, 3, 5, 10, 15, 20, 30]
```

核心函数：
```python
def mutate(config: dict, mutation_type: str = None) -> tuple[dict, str]
    # 返回 (new_config, mutation_description)
    # mutation_type 为 None 时随机选择

MUTATION_TYPES = [
    "add_filter",
    "remove_filter",
    "adjust_filter_threshold",
    "add_sorting",
    "adjust_sorting_weight",
    "adjust_holding_num",
    "adjust_rebalance_interval",
    "change_universe",
]
```

### 4. run_iteration.py

CLI 入口：
```
python run_iteration.py --base experiments/<name> --mutation-summary "..." [--mutation-type <type>]
```

流程：
1. 读 `state.json` → 读 `wizard_config.json`（champion）
2. 调用 `mutator.mutate()` 生成新配置
3. 保存临时配置到 `history/<iter_id>_config.json`
4. `wizard_executor.update_strategy()` + `run_backtest()`
5. `wait_for_completion()`
6. `fetch_results()` → `scorer.parse_backtest_result()` → `calculate_score()` → `decide_keep_rollback()`
7. keep 时：覆盖 `wizard_config.json`，更新 state.json
8. rollback 时：从 `history/<champion_iter>_config.json` 恢复 `wizard_config.json`
9. 写 `history/<iter_id>.json` + 追加 `history/iterations.tsv`

退出码：0=keep, 1=rollback, 2=crash

### 5. setup.py

```
python setup.py --name <experiment_name> --strategy-id <rq_strategy_id>
```

创建实验目录结构，从 `seed_wizard_config.json` 复制初始配置，生成初始 `state.json`。

---

## Data Models

### wizard_config.json（single_period 模板）

```json
{
  "name": "string",
  "template": "single_period",
  "universe": ["000300.XSHG"],
  "industries": ["*"],
  "board": ["*"],
  "stOption": "exclude",
  "filters": [
    {
      "operator": "less_than",
      "factor": {"type": "fundamental", "name": "pe_ratio"},
      "rhs": 15
    }
  ],
  "sorting": [
    {
      "factor": {"type": "fundamental", "name": "dividend_yield"},
      "ascending": false,
      "weight": 0.6
    }
  ],
  "maxHoldingNum": 15,
  "rebalanceInterval": 10,
  "backtest": {
    "start_date": "2021-01-01",
    "end_date": "2025-03-28",
    "capital": "100000",
    "benchmark": "000300.XSHG"
  },
  "objective": {
    "weights": {"calmar": 0.55, "sortino": 0.25, "information_ratio": 0.20},
    "hard_constraints": {"max_drawdown_limit": 0.35}
  },
  "loop": {
    "max_iterations": 100,
    "max_consecutive_failures": 5,
    "max_wait_seconds": 600
  }
}
```

### state.json

```json
{
  "current_iter": 0,
  "strategy_id": "123456",
  "champion_score": -1e308,
  "champion_iter": "",
  "champion_config": null,
  "champion_metrics": null,
  "consecutive_failures": 0,
  "last_update": "2025-01-01T00:00:00"
}
```

### history/<iter_id>.json

```json
{
  "iter": "0001",
  "backtest_id": "7973201",
  "status": "finished",
  "start_time": "2025-01-01T10:00:00",
  "end_time": "2025-01-01T10:05:00",
  "annual_return": 0.15,
  "max_drawdown": 0.12,
  "sharpe": 1.2,
  "sortino": 1.5,
  "information_ratio": 0.8,
  "score": 1.234,
  "decision": "keep",
  "reason": "new_score 1.234 > champion_score -inf",
  "mutation": "add_filter: pe_ratio < 20",
  "mutation_type": "add_filter",
  "fetch_result": {}
}
```

### history/iterations.tsv

```
iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation
0001\t7973201\tfinished\t0.1500\t0.1200\t1.20\t1.234000\tkeep\tadd_filter: pe_ratio < 20
```

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: 评分公式正确性

*For any* 有效的 ParsedMetrics（annual_return、max_drawdown、sortino、information_ratio 均为有限浮点数），`calculate_score()` 的返回值应严格等于 `calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20`，其中 `calmar = annual_return / max(abs(max_drawdown), 0.01)`。

**Validates: Requirements 5.2**

### Property 2: keep 决策条件

*For any* new_score 严格大于 champion_score，且回测状态为成功状态，且 max_drawdown 未超过硬约束，`decide_keep_rollback()` 应返回 `"keep"`。

**Validates: Requirements 5.3**

### Property 3: rollback 决策条件（硬约束）

*For any* `abs(max_drawdown) > max_drawdown_limit`，无论 score 高低，`decide_keep_rollback()` 应返回 `"rollback"`。

**Validates: Requirements 5.4**

### Property 4: rollback 决策条件（失败状态）

*For any* 回测状态不是 `finished` 或 `normal_exit` 的 metrics，`decide_keep_rollback()` 应返回 `"rollback"`。

**Validates: Requirements 5.5**

### Property 5: 变异后配置合法性

*For any* 合法的 wizard_config 和任意变异类型，`mutate()` 返回的新配置应满足：filters 中每个元素包含 operator、factor、rhs 字段；sorting 中每个元素包含 factor、ascending、weight 字段；maxHoldingNum 在 [5, 30] 范围内；rebalanceInterval 在 REBALANCE_OPTIONS 列表中。

**Validates: Requirements 3.2, 3.7**

### Property 6: add_filter 不重复因子

*For any* 合法的 wizard_config，执行 `add_filter` 变异后，新配置的 filters 数量应比原来多 1，且新增因子的 name 不在原 filters 的因子名列表中。

**Validates: Requirements 3.3**

### Property 7: adjust_filter_threshold 范围约束

*For any* 合法的 wizard_config（至少含一个 filter），执行 `adjust_filter_threshold` 变异后，被修改的 filter 的新 rhs 值应在原 rhs 值的 50%~180% 范围内（即 ±20%~±50% 调整后的合理区间）。

**Validates: Requirements 3.4**

### Property 8: adjust_sorting_weight 权重正数不变量

*For any* 合法的 wizard_config（至少含一个 sorting 规则），执行 `adjust_sorting_weight` 变异后，所有 sorting 规则的 weight 应均为正数。

**Validates: Requirements 8.4**

### Property 9: backtestId 解析正确性

*For any* 合法的 backtestId（纯数字字符串），将其嵌入格式字符串 `"回测已启动: <id>"` 后，`_extract_backtest_id()` 应能正确提取出原始 backtestId。

**Validates: Requirements 2.2**

### Property 10: 迭代记录 JSON 序列化往返

*For any* 迭代记录 dict（包含 iter、backtest_id、score、decision 等字段），将其写入 JSON 文件后再读取，所有字段的值应与原始 dict 完全一致。

**Validates: Requirements 6.2**

---

## Error Handling

### wizard_executor.py 错误处理

| 场景 | 处理方式 |
|------|---------|
| Node.js 脚本退出码非零 | 抛出 `WizardExecutorError`，包含 stdout+stderr |
| 无法从输出提取 backtestId | 等待 30s 后通过 HTTP API 查询最新回测 ID（fallback） |
| HTTP 轮询超时 | 抛出 `BacktestTimeoutError` |
| 回测以 error_exit 结束 | 抛出 `BacktestFailedError` |
| session 文件不存在 | 抛出 `WizardExecutorError`，提示用户登录 |

### run_iteration.py 错误处理

| 场景 | 退出码 | 处理方式 |
|------|--------|---------|
| strategy_id 为空 | 2 | 打印错误，退出 |
| update_strategy 失败 | 2 | 写 crash 记录，consecutive_failures +1 |
| run_backtest 失败 | 2 | 写 crash 记录，consecutive_failures +1 |
| wait_for_completion 超时 | 2 | 写 crash 记录，consecutive_failures +1 |
| 回测失败（error_exit） | 2 | 写 crash 记录，consecutive_failures +1 |
| score <= champion_score | 1 | rollback，恢复 wizard_config.json |
| max_drawdown 超限 | 1 | rollback，恢复 wizard_config.json |

### wizard_mutator.py 错误处理

| 场景 | 处理方式 |
|------|---------|
| remove_filter 但 filters 为空 | 自动切换到 add_filter |
| add_filter 但所有候选因子已使用 | 切换到 adjust_filter_threshold |
| adjust_sorting_weight 但 sorting 为空 | 切换到 add_sorting |
| change_universe 但只有一个选项 | 切换到 adjust_holding_num |

### 重启恢复

系统重启时，`run_iteration.py` 检查 state.json 与 history/ 的一致性：
- 若 `current_iter - 1` 对应的 history 文件不存在，回退 `current_iter` 并从 `history/<champion_iter>_config.json` 恢复 `wizard_config.json`
- 若 champion_iter 对应的 history 文件不存在，清空 champion 信息

---

## Testing Strategy

### 单元测试（example-based）

针对具体场景的确定性测试：

- `test_setup.py`：验证初始化后的目录结构和文件内容
- `test_state_json_fields.py`：验证 state.json 初始字段和值
- `test_keep_updates_files.py`：验证 keep 决策后文件正确更新
- `test_rollback_restores_config.py`：验证 rollback 后 wizard_config.json 恢复正确
- `test_tsv_format.py`：验证 iterations.tsv 格式正确
- `test_recovery_on_restart.py`：验证重启恢复逻辑

### 属性测试（property-based）

使用 [Hypothesis](https://hypothesis.readthedocs.io/) 进行属性测试，最少 100 次迭代：

```python
# 每个属性测试的标注格式
# Feature: autoresearch-ricequant-wizard, Property N: <property_text>
```

- `test_scorer_properties.py`：Property 1、2、3、4
- `test_mutator_properties.py`：Property 5、6、7、8
- `test_executor_properties.py`：Property 9
- `test_history_properties.py`：Property 10

### 集成测试

使用 mock 替代外部依赖（Node.js subprocess、HTTP API）：

- `test_run_iteration_integration.py`：mock wizard_executor，验证完整迭代流程
- `test_wait_for_completion_mock.py`：mock HTTP 响应，验证状态机逻辑

### 不适用 PBT 的场景

以下场景使用 example-based 测试或 smoke 测试：
- 文件系统操作（初始化目录、写入文件）
- Node.js subprocess 调用（外部依赖）
- HTTP API 轮询（外部服务）
- CLI 参数解析（接口存在性）
