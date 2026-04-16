# autoresearch_joinquant_factor 技术升级方案

## 背景

当前 `autoresearch_joinquant_factor` 目录缺少与其他 autoresearch（如 `autoresearch_joinquant`、`autoresearch_ricequant`、`autoresearch_10jqka_backtest`）一致的标准结构和功能。

---

## 升级目标

1. 增加 `iterations.tsv` 历史记录文件
2. 调整默认回测区间：训练 1 年 + 回测最近 3 个月
3. 提升 `setup.py` 策略代码质量
4. 完善 `program.md` 文档结构

---

## 详细方案

### 1. 增加 iterations.tsv 文件

**当前状态**：无 `iterations.tsv` 文件

**新增位置**：根目录下
```
strategy_autoresearch_factor_<name>/
├── strategy.py
├── search_notes.md
├── iterations.tsv    ← 新增（根目录）
└── program.md
```

**iterations.tsv 格式**：
```
iter	score	diversity	decision	mutation
0000	0.3256	0.75	keep	【L0-建立基准】初始因子组合 ['size','roe_ttm','momentum']
0001	0.3412	0.80	keep	【L1-因子变异】替换 momentum→beta
```

**实施步骤**：
- 在 `setup.py` 中增加 `init_iterations_tsv()` 函数
- 在 `run_iteration.py` 中增加 `append_tsv()` 函数
- 每次迭代后将结果追加到根目录的 `iterations.tsv`

---

### 2. 调整默认回测区间

**当前配置**：
```python
def _default_dates():
    today = datetime.today()
    end = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    start = (today - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
    return start, end
```

**新配置**：
```python
def _default_dates():
    today = datetime.today()
    # 回测结束日期：最近一周（确保数据完整）
    backtest_end = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    # 回测开始日期：最近 3 个月
    backtest_start = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    # 训练开始日期：最近 1 年
    train_start = (today - timedelta(days=365)).strftime("%Y-%m-%d")
    return train_start, backtest_start, backtest_end
```

**策略代码调整**：
- 训练区间：`train_start` ~ `backtest_start`（约 1 年）
- 回测区间：`backtest_start` ~ `backtest_end`（约 3 个月）
- 原来的 `train_len = int(len(dateList) * 0.66)` 改为显式计算

**修改 strategy.py 主函数**：
```python
def main():
    train_start = "{train_start}"
    backtest_start = "{backtest_start}"
    backtest_end = "{backtest_end}"
    
    peroid = "W"
    dateList = get_period_date(peroid, train_start, backtest_end)
    
    # 显式计算训练和回测的分界点
    train_dateList = [d for d in dateList if d <= backtest_start]
    test_dateList = [d for d in dateList if d > backtest_start]
    
    # 训练数据（1 年）
    for date in train_dateList:
        ...
    
    # 回测数据（3 个月）
    for date in test_dateList:
        ...
```

---

### 3. 提升 setup.py 策略代码

**当前问题**：
- `calculate_diversity()` 函数中的 `FACTOR_CATEGORIES` 硬编码过长（200+ 行）
- 缺少 `history/` 目录初始化
- 缺少 `iterations.tsv` 初始化和追加逻辑

**改进方案**：

#### 3.1 拆分因子分类到独立文件

创建 `factor_categories.py`（已存在），将完整的因子分类定义移入：
```python
FACTOR_CATEGORIES = {
    "basics": [...],
    "emotion": [...],
    ...
}

FACTOR_TO_CAT = {}
for cat, fs in FACTOR_CATEGORIES.items():
    for f in fs:
        FACTOR_TO_CAT[f] = cat
```

在 `strategy.py` 中 import：
```python
from factor_categories import FACTOR_TO_CAT
```

#### 3.2 增加 iterations.tsv 初始化（根目录）

```python
def init_iterations_tsv(base: Path) -> None:
    tsv = base / "iterations.tsv"
    if not tsv.exists():
        tsv.write_text(TSV_HEADER, encoding="utf-8")

TSV_HEADER = "iter\tscore\tdiversity\tdecision\tmutation\n"
```

#### 3.3 增加 append_tsv() 函数

```python
def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "iterations.tsv"
    line = "\t".join([
        str(row.get("iter", "")),
        f"{row.get('score', 0):.4f}",
        f"{row.get('diversity', 0):.2f}",
        str(row.get("decision", "")),
        str(row.get("mutation", "")),
    ]) + "\n"
    with open(tsv, "a", encoding="utf-8") as f:
        f.write(line)
```

#### 3.4 增加 baseline 运行和记录逻辑

参考 `autoresearch_joinquant/setup.py` 的 `run_baseline()` 函数：
- 执行回测 → 评分 → 写入 search_notes.md 和 iterations.tsv

---

### 4. 完善 program.md 文档结构

**当前结构**（170 行）：缺少 `iterations.tsv` 文件说明

**参考标准**（autoresearch_10jqka_backtest/program.md）：

```markdown
## 目录结构

```
strategy_autoresearch_factor_<name>/
├── strategy.py        ← 唯一文件，包含因子组合+评估代码
├── search_notes.md    ← 状态 + 历史 + 搜索地图
├── iterations.tsv     ← 只读，由 run_iteration.py 维护
└── program.md         ← 本文件（只读）
```
```

**改进内容**：
1. 增加 `iterations.tsv` 文件说明
2. 增加 `iterations.tsv` 查看指令：`cat iterations.tsv`
3. 更新实验循环中读取历史的方式
4. 增加更详细的停止条件和分析要求

---

## 实施计划

| 步骤 | 内容 | 文件 | 预估工作量 |
|------|------|------|-----------|
| 1 | 增加 `init_iterations_tsv()` 和 `append_tsv()` | setup.py, run_iteration.py | 25 行 |
| 2 | 调整默认日期配置 | setup.py | 10 行 |
| 3 | 重构 strategy 模板的日期处理 | setup.py (STRATEGY_TEMPLATE) | 20 行 |
| 4 | 将因子分类移入独立文件引用 | setup.py | 5 行 |
| 5 | 完善 program.md 目录结构说明 | program.md | 10 行 |
| 6 | 增加 iterations.tsv 查看指令 | program.md | 5 行 |

**总预估工作量**：约 75 行代码修改

---

## 验证方案

升级完成后运行测试：
```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_joinquant_factor
python setup.py --name test_upgrade --pool small
cat strategy_autoresearch_factor_test_upgrade_*/iterations.tsv
```

验证点：
1. `iterations.tsv` 存在于根目录
2. 有 baseline 记录
3. 回测区间为训练 1 年 + 回测 3 个月
4. `program.md` 包含 `iterations.tsv` 说明

---

## 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| setup.py | 修改 | 增加 iterations.tsv 初始化、调整日期、重构策略模板 |
| run_iteration.py | 修改 | 增加 append_tsv() |
| program.md | 修改 | 增加 iterations.tsv 说明 |
| factor_categories.py | 保持 | 已存在，确认引用方式正确 |

---

## 参考文件

- `/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_joinquant/setup.py`
- `/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_joinquant/program.md`
- `/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_10jqka_backtest/setup.py`
- `/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_10jqka_backtest/program.md`