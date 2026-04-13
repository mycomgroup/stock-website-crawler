# Wizard Strategy Autoresearch

向导式策略自动迭代优化系统。通过 JSON 配置参数优化，agent 自主循环迭代，全程留档可追溯。

---

## 系统概述

本系统优化 **RiceQuant 向导式策略的 JSON 配置参数**，而非 Python 代码。通过 8 种变异类型自动探索参数空间，寻找最优配置。

---

## 文件结构

```
skills/autoresearch_ricequant-wizard/
├── setup.py                # 初始化 + 运行 baseline
├── run_iteration.py        # 迭代脚本
├── wizard_executor.py      # RiceQuant API 封装
├── wizard_mutator.py       # 8 种配置变异逻辑
├── scorer.py               # 评分 + keep/rollback 决策
├── analyze.py              # 结果分析工具
├── validate.py             # 配置验证工具
├── seed_config.json        # 种子配置（低估值高股息）
├── seed_smallcap_value.json    # 小盘价值种子
├── seed_largecap_growth.json   # 大盘成长种子
├── seed_dividend.json          # 高股息红利种子
├── SEED_TEMPLATE.md        # 种子配置模板
├── program.md              # agent 行动规则
└── experiments/<name>/     # 实验子目录
    ├── wizard_config.json  ← 当前 champion 配置
    ├── state.json          ← 当前状态
    └── history/            ← 迭代历史
```

---

## 快速开始

### Step 1：初始化实验

```bash
cd skills/autoresearch_ricequant-wizard

# Mock 模式（模拟数据，快速验证）
python setup.py --name my_experiment --mock

# 真实回测（需要 RiceQuant 策略 ID）
python setup.py --name my_experiment --strategy-id 2421275

# 指定种子文件
python setup.py --name smallcap_test --seed seed_smallcap_value.json --mock
```

### 可用种子文件

| 种子文件 | 策略方向 | 股票池 |
|---------|---------|--------|
| `seed_config.json` | 低估值高股息 | 沪深300 |
| `seed_smallcap_value.json` | 小盘价值 | 中证1000 |
| `seed_largecap_growth.json` | 大盘成长 | 沪深300 |
| `seed_dividend.json` | 高股息红利 | 沪深300 |

### Step 2：运行迭代

```bash
python run_iteration.py \
    --base experiments/my_experiment \
    --mutation-summary "【add_filter】新增 roe > 10 过滤低质量公司" \
    --mutation-type add_filter
```

### Step 3：查看进度

```bash
cat experiments/my_experiment/history/iterations.tsv
python analyze.py --base experiments/my_experiment
```

---

## 评分公式

```python
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

新 score 严格大于 champion score 才 keep，否则 rollback。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。

---

## 详细文档

- [WIZARD_GUIDE.md](./WIZARD_GUIDE.md) - 完整使用指南（配置结构、因子库、变异类型、技术架构）
- [program.md](./program.md) - Agent 操作指南
- [MOCK_MODE.md](./MOCK_MODE.md) - Mock 模式说明

---

## 相关资源

- [autoresearch_ricequant](../autoresearch_ricequant/README.md) - 代码策略自动优化系统
- [ricequant-wizard](../ricequant-wizard/README.md) - RiceQuant 向导式策略工具集
