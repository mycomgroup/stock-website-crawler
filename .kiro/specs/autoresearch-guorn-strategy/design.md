# 设计文档: autoresearch-guorn-strategy

## 概述

autoresearch-guorn-strategy 是一个针对果仁网量化交易策略的自动化参数优化框架。系统将经过验证的 autoresearch_ricequant-wizard 架构适配到果仁网基于 Node.js 的策略执行基础设施上,通过变异、回测和评分实现策略参数的自主迭代优化。

### 与 autoresearch-ricequant-wizard 的关键差异

| 维度 | autoresearch-ricequant-wizard | autoresearch-guorn-strategy |
|------|-------------------------------|----------------------------|
| 目标平台 | RiceQuant (ricequant.com) | 果仁网 (guorn.com) |
| 策略格式 | wizard_config.json | guorn_strategy_config.json |
| 执行接口 | subprocess 调用 Node.js + HTTP API | 直接调用 guorn_strategy skill |
| 因子库 | RiceQuant 因子 (~20个) | 果仁指标库 (~100+ 函数 + 常用指标) |
| 会话管理 | ricequant_strategy/data/session.json | guorn_strategy/data/session.json |
| 回测触发 | run-skill.js --update + --run | strategy-runner.js runBacktestViaBrowser |

---

## 系统架构

```
skills/autoresearch_guorn_strategy/
├── scorer.py                    # 评分模块（复用 ricequant-wizard 逻辑）
├── guorn_executor.py            # 执行器：调用 guorn_strategy skill
├── guorn_mutator.py             # 变异器：8种策略参数变异类型
├── run_iteration.py             # 单次迭代执行器（CLI 入口）
├── init_experiment.py           # 初始化实验目录
├── seed_config.json             # 种子配置（示例策略）
├── program.md                   # agent 操作指南
└── experiments/
    └── <experiment_name>/
        ├── guorn_config.json    # 当前 champion 配置
        ├── state.json           # 迭代状态
        └── history/
            ├── iterations.tsv
            ├── search_notes.md
            ├── 0000_config.json
            ├── 0000.json
            └── ...
```

### 数据流

```
agent
  │
  ▼
run_iteration.py  ──读──▶  state.json
  │                        guorn_config.json (champion)
  │
  ├──▶ guorn_mutator.py  ──生成──▶  candidate_config (临时)
  │
  ├──▶ guorn_executor.py
  │       │
  │       ├── 调用 guorn_strategy/request/strategy-runner.js
  │       │       └── runBacktestViaBrowser(config, sessionFile)
  │       │           ├── 启动 Playwright 浏览器
  │       │           ├── 注入 session cookies
  │       │           ├── 执行 scrat.utility.ajaxDispatch('POST', 'stock/runtest', ...)
  │       │           └── 轮询 window.__backtestResult（最多 90 秒）
  │       │
  │       └── 提取回测结果（annualReturn, maxDrawdown, winRate, informationRatio 等）
  │
  ├──▶ scorer.py  ──计算──▶  score, decision
  │
  └──▶ keep/rollback
          ├── keep:     覆盖 guorn_config.json，写 history/<iter>_config.json
          └── rollback: 从 history/<champion_iter>_config.json 恢复 guorn_config.json
```

---

## 组件设计与接口

### 1. scorer.py

复用 autoresearch_ricequant-wizard 的评分逻辑，适配果仁网的指标字段名。

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
    win_rate: float
    avg_holding_days: float
    sell_count: int

def parse_backtest_result(result_json: dict) -> ParsedMetrics
    # 从果仁回测结果中提取指标
    # result_json.data.trade_summary.winsorize_annual → annual_return
    # result_json.data.trade_summary.win_ratio → win_rate
    # result_json.data.trade_summary.year_information_ratio → information_ratio

def calculate_score(metrics: ParsedMetrics, weights: dict = None) -> float
    # calmar × 0.55 + sortino × 0.25 + information_ratio × 0.20
    # calmar = annual_return / max(abs(max_drawdown), 0.01)

def decide_keep_rollback(
    new_score: float,
    champion_score: float,
    new_metrics: ParsedMetrics,
    champion_metrics: Optional[ParsedMetrics],
    hard_constraints: dict = None
) -> tuple[str, str]  # (decision, reason)
    # 硬约束：abs(max_drawdown) > 0.35 → rollback
    # new_score > champion_score → keep
    # 否则 → rollback
```

### 2. guorn_executor.py

路径常量：
```python
GUORN_SKILL_DIR = Path(__file__).parent.parent / "guorn_strategy"
SESSION_FILE = GUORN_SKILL_DIR / "data" / "session.json"
```

核心函数：
```python
def run_backtest(config: dict, session_file: str = None) -> dict:
    """
    通过 guorn_strategy skill 执行回测
    
    Args:
        config: 策略配置，包含 filters, ranks, pool, start, end 等字段
        session_file: session.json 路径（可选，默认使用 GUORN_SKILL_DIR/data/session.json）
    
    Returns:
        {
            "status": "ok",
            "backtest_id": str,  # calc_id
            "summary": {
                "annualReturn": float,
                "maxDrawdown": float,
                "winRate": float,
                "informationRatio": float,
                "avgHoldingDays": float,
                "sellCount": int,
                ...
            },
            "full_result": dict  # 完整的果仁回测结果
        }
    
    Raises:
        GuornExecutorError: 回测失败时抛出
        BacktestTimeoutError: 回测超时时抛出
    """
    # 1. 验证 session 文件存在
    # 2. 调用 strategy-runner.js 的 runStrategyWorkflow
    # 3. 解析结果并映射字段名
    # 4. 返回标准化的结果格式

def validate_session(session_file: str = None) -> dict:
    """
    验证 session 文件有效性
    
    Returns:
        {
            "valid": bool,
            "username": str,
            "level": int,  # 1=普通账号（回测窗口约1年）
            "cookies": list
        }
    """

def normalize_config(config: dict) -> dict:
    """
    规范化策略配置为果仁格式
    
    - 将高级字段名（filters, rankings, pool）转换为果仁内部格式
    - 使用参数缓存解析因子名称和股票池名称
    - 验证配置合法性
    """
```

异常类：
```python
class GuornExecutorError(Exception): pass
class BacktestTimeoutError(GuornExecutorError): pass
class BacktestFailedError(GuornExecutorError): pass
class SessionInvalidError(GuornExecutorError): pass
```

### 3. guorn_mutator.py

因子候选库（基于 GUORN_INDICATORS_CATALOG.md）：
```python
# 系统函数示例
SYSTEM_FUNCTIONS = {
    "MA": {"expression": "MA(收盘价,{days})", "type": "time_window", "params": {"days": [5, 10, 20, 60]}},
    "Stdev": {"expression": "Stdev(1日涨幅,{days})", "type": "time_window", "params": {"days": [20, 60]}},
    "Slope": {"expression": "Slope(收盘价,{days})", "type": "regression", "params": {"days": [20, 60]}},
}

# 常用指标示例
COMMON_INDICATORS = {
    "pe_ttm": {"name": "市盈率", "type": "fundamental", "operators": ["<", ">"], "range": [5, 80], "default": 20},
    "pb": {"name": "市净率", "type": "fundamental", "operators": ["<", ">"], "range": [0.5, 5], "default": 2},
    "roe": {"name": "净资产收益率", "type": "fundamental", "operators": [">"], "range": [5, 30], "default": 10},
    "dividend_yield": {"name": "股息率", "type": "fundamental", "operators": [">"], "range": [1, 8], "default": 2},
    "turnover_rate": {"name": "换手率", "type": "pricing", "operators": ["<", ">"], "range": [0.5, 10], "default": 2},
    "macd_golden_cross": {"name": "MACD金叉", "type": "technical", "operators": ["="], "range": [0, 1], "default": 1},
}

POOL_OPTIONS = ["hs300", "zz500", "zz1000", "all"]  # 映射到果仁股票池 ID
HOLDING_NUM_OPTIONS = [5, 10, 15, 20, 25, 30]
REBALANCE_OPTIONS = [1, 3, 5, 10, 15, 20, 30]
```

核心函数：
```python
def mutate(config: dict, mutation_type: str = None) -> tuple[dict, str]:
    """
    生成候选配置
    
    Args:
        config: 当前配置
        mutation_type: 变异类型（可选，None 时随机选择）
    
    Returns:
        (new_config, mutation_description)
    
    Mutation Types:
        - add_filter: 添加筛选条件
        - remove_filter: 移除筛选条件
        - adjust_filter_threshold: 调整筛选阈值（±20%~±50%）
        - add_ranking: 添加排序规则
        - adjust_ranking_weight: 调整排序权重
        - adjust_holding_num: 调整持仓数量
        - adjust_rebalance_interval: 调整调仓间隔
        - change_pool: 更换股票池
    """

def load_factor_library(catalog_path: str = None) -> dict:
    """
    从 GUORN_INDICATORS_CATALOG.md 加载因子库
    
    Returns:
        {
            "system_functions": {...},
            "common_indicators": {...}
        }
    """

def validate_config(config: dict) -> bool:
    """
    验证配置合法性
    
    - filters 格式正确
    - rankings 格式正确
    - pool 在可选列表中
    - holding_num 在合理范围内
    - rebalance_interval 在可选列表中
    """
```

### 4. run_iteration.py

CLI 入口：
```bash
python run_iteration.py --base experiments/<name> --mutation-summary "..." [--mutation-type <type>]
```

流程：
1. 读取 `state.json` 和 `guorn_config.json`（champion）
2. 调用 `guorn_mutator.mutate()` 生成候选配置
3. 保存临时配置到 `history/<iter_id>_config.json`
4. 调用 `guorn_executor.run_backtest()`
5. 调用 `scorer.parse_backtest_result()` → `calculate_score()` → `decide_keep_rollback()`
6. keep 时：覆盖 `guorn_config.json`，更新 `state.json`
7. rollback 时：从 `history/<champion_iter>_config.json` 恢复 `guorn_config.json`
8. 写入 `history/<iter_id>.json` 和追加 `history/iterations.tsv`
9. Git commit 变更

退出码：
- 0: keep
- 1: rollback
- 2: crash

### 5. init_experiment.py

```bash
python init_experiment.py --name <experiment_name> --seed-config <path>
```

创建实验目录结构：
```
experiments/<experiment_name>/
├── guorn_config.json      # 从 seed_config.json 复制
├── state.json             # 初始状态
├── program.md             # agent 指南
├── README.md              # 实验说明
└── history/
    ├── iterations.tsv     # 列标题
    └── search_notes.md    # 搜索笔记模板
```

初始化 Git 仓库并提交基准配置。

---

## 数据模型

### guorn_config.json

```json
{
  "name": "低估值高股息策略",
  "filters": [
    {
      "factor": "pe_ttm",
      "operator": "<",
      "value": 15
    },
    {
      "factor": "dividend_yield",
      "operator": ">",
      "value": 2
    }
  ],
  "rankings": [
    {
      "factor": "dividend_yield",
      "ascending": false,
      "weight": 0.6
    },
    {
      "factor": "roe",
      "ascending": false,
      "weight": 0.4
    }
  ],
  "pool": "hs300",
  "exclude_st": true,
  "holding_num": 15,
  "rebalance_interval": 10,
  "backtest": {
    "start": "2021-01-01",
    "end": "2025-03-28",
    "benchmark": "hs300",
    "trade_cost": 0.002
  },
  "objective": {
    "weights": {
      "calmar": 0.55,
      "sortino": 0.25,
      "information_ratio": 0.20
    },
    "hard_constraints": {
      "max_drawdown_limit": 0.35
    }
  },
  "loop": {
    "max_iterations": 100,
    "max_consecutive_failures": 5,
    "max_wait_seconds": 90
  }
}
```

### state.json

```json
{
  "current_iter": 0,
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
  "backtest_id": "uid.1234567890",
  "status": "ok",
  "start_time": "2025-01-01T10:00:00",
  "end_time": "2025-01-01T10:05:00",
  "annual_return": 0.15,
  "max_drawdown": 0.12,
  "win_rate": 0.65,
  "information_ratio": 0.8,
  "avg_holding_days": 25,
  "sell_count": 120,
  "score": 1.234,
  "decision": "keep",
  "reason": "new_score 1.234 > champion_score -inf",
  "mutation": "add_filter: pe_ttm < 20",
  "mutation_type": "add_filter",
  "full_result": {}
}
```

### history/iterations.tsv

```
iter	backtest_id	status	annual_return	max_drawdown	win_rate	score	decision	mutation
0001	uid.1234567890	ok	0.1500	0.1200	0.65	1.234000	keep	add_filter: pe_ttm < 20
```

---

## 正确性属性

### 属性 1: 评分公式正确性

*For any* 有效的 ParsedMetrics，`calculate_score()` 的返回值应严格等于 `calmar × 0.55 + sortino × 0.25 + information_ratio × 0.20`，其中 `calmar = annual_return / max(abs(max_drawdown), 0.01)`。

**验证需求**: 需求 4.1, 4.2

### 属性 2: keep 决策条件

*For any* new_score 严格大于 champion_score，且回测状态为成功，且 max_drawdown 未超过硬约束，`decide_keep_rollback()` 应返回 `"keep"`。

**验证需求**: 需求 5.4

### 属性 3: rollback 决策条件（硬约束）

*For any* `abs(max_drawdown) > max_drawdown_limit`，无论 score 高低，`decide_keep_rollback()` 应返回 `"rollback"`。

**验证需求**: 需求 5.3

### 属性 4: 变异后配置合法性

*For any* 合法的 guorn_config 和任意变异类型，`mutate()` 返回的新配置应满足：filters 中每个元素包含 factor、operator、value 字段；rankings 中每个元素包含 factor、ascending、weight 字段。

**验证需求**: 需求 2.1, 2.7

### 属性 5: add_filter 不重复因子

*For any* 合法的 guorn_config，执行 `add_filter` 变异后，新配置的 filters 数量应比原来多 1，且新增因子不在原 filters 的因子列表中。

**验证需求**: 需求 2.5

### 属性 6: adjust_filter_threshold 范围约束

*For any* 合法的 guorn_config（至少含一个 filter），执行 `adjust_filter_threshold` 变异后，被修改的 filter 的新 value 应在原 value 的 50%~180% 范围内。

**验证需求**: 需求 2.6

### 属性 7: 迭代记录 JSON 序列化往返

*For any* 迭代记录 dict，将其写入 JSON 文件后再读取，所有字段的值应与原始 dict 完全一致。

**验证需求**: 需求 7.4, 7.5

---

## 错误处理

### guorn_executor.py 错误处理

| 场景 | 处理方式 |
|------|---------|
| session 文件不存在 | 抛出 `SessionInvalidError`，提示运行 ensure-session.js |
| session 过期 | 抛出 `SessionInvalidError`，提示重新登录 |
| 回测超时（90秒） | 抛出 `BacktestTimeoutError` |
| 回测失败（status != 'ok'） | 抛出 `BacktestFailedError` |
| 浏览器启动失败 | 抛出 `GuornExecutorError` |

### run_iteration.py 错误处理

| 场景 | 退出码 | 处理方式 |
|------|--------|---------|
| 配置文件不存在 | 2 | 打印错误，退出 |
| run_backtest 失败 | 2 | 写 crash 记录，consecutive_failures +1 |
| 回测超时 | 2 | 写 crash 记录，consecutive_failures +1 |
| score <= champion_score | 1 | rollback，恢复 guorn_config.json |
| max_drawdown 超限 | 1 | rollback，恢复 guorn_config.json |

### guorn_mutator.py 错误处理

| 场景 | 处理方式 |
|------|---------|
| remove_filter 但 filters 为空 | 切换到 add_filter |
| add_filter 但所有候选因子已使用 | 切换到 adjust_filter_threshold |
| adjust_ranking_weight 但 rankings 为空 | 切换到 add_ranking |
| change_pool 但只有一个选项 | 切换到 adjust_holding_num |

### 模拟模式

当 `GUORN_MOCK_MODE=1` 时：
- 跳过真实浏览器自动化
- 基于配置复杂度生成模拟指标
- 模拟延迟：配置更新 0.5s，回测提交 1s，完成 2s
- 生成合理范围的指标：annualReturn [0.08, 0.25]，maxDrawdown [0.05, 0.15]

---

## 测试策略

### 单元测试（example-based）

- `test_init_experiment.py`: 验证初始化后的目录结构
- `test_state_json_fields.py`: 验证 state.json 初始字段
- `test_keep_updates_files.py`: 验证 keep 决策后文件更新
- `test_rollback_restores_config.py`: 验证 rollback 后配置恢复
- `test_tsv_format.py`: 验证 iterations.tsv 格式

### 属性测试（property-based）

使用 Hypothesis 进行属性测试，最少 100 次迭代：

```python
# Feature: autoresearch-guorn-strategy, Property N: <property_text>
```

- `test_scorer_properties.py`: 属性 1、2、3
- `test_mutator_properties.py`: 属性 4、5、6
- `test_history_properties.py`: 属性 7

### 集成测试

使用 mock 替代外部依赖：

- `test_run_iteration_integration.py`: mock guorn_executor，验证完整迭代流程
- `test_mock_mode.py`: 验证模拟模式行为

---

## 与现有 guorn_strategy skill 的集成

### 依赖关系

```
autoresearch_guorn_strategy/
├── guorn_executor.py
│   └── 调用 → skills/guorn_strategy/request/strategy-runner.js
│       └── 使用 → skills/guorn_strategy/data/session.json
│
└── guorn_mutator.py
    └── 读取 → skills/guorn_strategy/GUORN_INDICATORS_CATALOG.md
```

### 配置规范化流程

```
高级配置（guorn_config.json）
  │
  ▼
guorn_executor.normalize_config()
  │
  ├── 解析因子名称 → 果仁内部 ID（使用参数缓存）
  ├── 解析股票池名称 → 果仁股票池 ID
  ├── 转换 filters 格式 → 果仁字符串格式
  └── 转换 rankings 格式 → 果仁 rank 格式
  │
  ▼
strategy-runner.js normalizeConfig()
  │
  └── 最终果仁 API 格式
```

### 会话管理

- 复用 `skills/guorn_strategy/data/session.json`
- 如果 session 不存在或过期，提示用户运行：
  ```bash
  cd skills/guorn_strategy
  node request/ensure-session.js
  ```

---

## 部署与运行

### 环境要求

- Python 3.10+
- Node.js 18+
- Playwright（已安装 chromium）
- 有效的果仁网账号（level=1 普通账号即可）

### 初始化实验

```bash
cd skills/autoresearch_guorn_strategy
python init_experiment.py --name my_experiment --seed-config seed_config.json
```

### 运行单次迭代

```bash
python run_iteration.py \
  --base experiments/my_experiment \
  --mutation-summary "添加市净率筛选" \
  --mutation-type add_filter
```

### Agent 自动化循环

参考 `program.md` 中的指令，agent 应：
1. 读取 `state.json` 和 `history/iterations.tsv`
2. 分析历史记录，更新 `search_notes.md`
3. 选择变异类型
4. 执行 `run_iteration.py`
5. 检查停止条件（consecutive_failures >= 5 或 current_iter >= 100）
6. 重复步骤 1-5

---

## 附录

### 果仁网 API 限制

- 普通账号（level=1）：回测时间窗口约 1 年
- 回测必须通过浏览器 JS 执行（scrat.utility.ajaxDispatch）
- 直接 HTTP POST 会返回 Server Error

### 参数缓存

参数缓存用于将人类可读的因子名称映射到果仁内部 ID：

```json
{
  "factors": {
    "pe_ttm": "股票每日指标_市盈率",
    "pb": "股票每日指标_市净率",
    "roe": "股票每日指标_资权益回报率",
    ...
  },
  "pools": {
    "hs300": "沪深300",
    "zz500": "中证500",
    "zz1000": "中证1000",
    ...
  }
}
```

### 因子库扩展

要添加新因子：
1. 在 `guorn_mutator.py` 的 `COMMON_INDICATORS` 中添加条目
2. 在参数缓存中添加映射关系
3. 验证因子在果仁网上可用

