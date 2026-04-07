# Strategy Autoresearch

量化策略自动迭代优化系统。输入一个 RiceQuant 单文件策略，agent 自主循环迭代优化，全程留档可追溯。

---

## 文件结构

```
skills/autoresearch/
├── setup.py              # Step 1：初始化 + 运行 baseline
├── run_iteration.py      # agent 每轮调用
├── ricequant_executor.py # RiceQuant HTTP API 封装
├── scorer.py             # 评分 + keep/rollback 决策
├── preflight_checker.py  # 策略文件预检查
├── program.md            # agent 行动规则
└── strategy_autoresearch_<策略名>/   # 实验子目录
    ├── strategy.py        ← 唯一策略文件，agent 直接在这里改
    ├── seed_config.json   ← 只读
    ├── state.json         ← 当前状态（champion 得分、迭代编号）
    ├── program.md         ← agent 行动规则副本
    └── history/
        ├── iterations.tsv
        ├── 0000_baseline.json
        └── 0001.json, ...
```

---

## 快速开始

### Step 1：初始化 + 运行 Baseline（一条命令）

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch
python setup.py --strategy-file /path/to/your/strategy.py
```

可选参数：
- `--name my_strategy` — 自定义策略名（默认取文件名）
- `--start-date 2021-01-01` — 回测开始日期
- `--end-date 2025-03-28` — 回测结束日期
- `--capital 100000` — 初始资金
- `--benchmark 000300.XSHG` — 基准指数

脚本自动完成：
1. 在 RiceQuant 创建/复用 `autoresearch_<name>` 策略，获取 strategy_id
2. 在实验目录生成 `seed_config.json`
3. 创建目录结构，复制策略为 `strategy.py`
4. 提交 baseline 回测，等待结果，写入 `state.json` 和 `history/`

### Step 2：运行自动迭代

在实验子目录下启动 agent，直接读 `program.md`：

```
请阅读 program.md，然后开始迭代优化循环。
```

agent 的工作目录就是实验子目录本身，所有相对路径（`strategy.py`、`state.json`、`history/`）都正确。

### Step 3：查看进度

```bash
cat strategy_autoresearch_rfscore7_pb10_rq/history/iterations.tsv
```

---

## 评分公式

```
score = annual_return * 0.45 - abs(max_drawdown) * 0.30 + sharpe * 0.20 + win_rate * 0.05
```

新 score 严格大于 champion score 才 keep，否则 rollback。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。
