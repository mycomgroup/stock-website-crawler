# autoresearch-guorn-strategy

果仁网策略参数自动迭代优化系统。输入种子配置，agent 自主循环迭代优化，全程留档可追溯。

---

## 文件结构

```
skills/autoresearch_guorn_strategy/
├── setup.py              # Step 1：初始化实验
├── run_iteration.py      # agent 每轮调用
├── guorn_executor.py     # 果仁网回测执行器
├── guorn_mutator.py      # 8 种变异类型
├── scorer.py             # 评分 + keep/rollback 决策
├── seed_config.json      # 默认种子配置
├── SEED_TEMPLATE.md      # 自然语言配置模板
├── program.md            # agent 行动规则
└── experiments/
    └── <experiment_name>/
        ├── guorn_config.json  ← 当前 champion 配置
        ├── state.json         ← 当前状态（champion 得分、迭代编号）
        ├── program.md         ← agent 行动规则副本
        └── history/
            ├── iterations.tsv
            ├── search_notes.md
            ├── 0000_config.json
            └── 0001.json, ...
```

---

## 快速开始

### Step 1：初始化实验

```bash
cd skills/autoresearch_guorn_strategy

# 使用默认种子配置（低估值高股息策略）
python setup.py --name my_experiment

# 或使用自定义种子配置
python setup.py --name my_experiment --seed-config custom_seed.json
```

脚本自动完成：
1. 创建实验目录结构
2. 复制种子配置到 `guorn_config.json`
3. 初始化 `state.json` 和 `history/`
4. 生成 `program.md` 和 `README.md`
5. 初始化 Git 仓库

### Step 2：运行自动迭代

在实验子目录下启动 agent，直接读 `program.md`：

```
请阅读 program.md，然后开始迭代优化循环。
```

agent 的工作目录就是实验子目录本身，所有相对路径（`guorn_config.json`、`state.json`、`history/`）都正确。

### Step 3：查看进度

```bash
cat experiments/my_experiment/history/iterations.tsv
```

---

## 评分公式

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

新 score 严格大于 champion score 才 keep，否则 rollback。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。

---

## 8 种变异类型

1. **add_filter**: 添加筛选条件
2. **remove_filter**: 移除筛选条件
3. **adjust_filter_threshold**: 调整筛选阈值（±20%~±50%）
4. **add_ranking**: 添加排序规则
5. **adjust_ranking_weight**: 调整排序权重
6. **adjust_holding_num**: 调整持仓数量
7. **adjust_rebalance_interval**: 调整调仓间隔
8. **change_pool**: 更换股票池

---

## 环境要求

1. 确保 guorn_strategy skill 已配置：

```bash
cd skills/guorn_strategy
node request/ensure-session.js
```

2. 验证 session 有效：

```bash
cd skills/autoresearch_guorn_strategy
python -c "from guorn_executor import validate_session; print(validate_session())"
```

---

## 模拟模式

用于测试，无需真实 API 调用：

```bash
export GUORN_MOCK_MODE=1
python setup.py --name test_experiment
```
