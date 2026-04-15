# Skills 问题审计（2026-04-15）

> 结论标签：
> - **存在**：代码中可直接复现
> - **部分存在**：问题描述有偏差，但确有相关风险
> - **不存在**：描述与当前代码不符

## 1) max_drawdown 正负号定义不一致（JoinQuant / RiceQuant）

- 结论：**存在**。
- 证据：
  - `ParsedMetrics` 注释写“平台返回正值，如 `0.15` 表示 `-15%` 回撤”。
  - `decide_keep_rollback` 注释写“`max_drawdown` 是负值（如 `-0.15`）”。
  - 计算和约束处虽然都用了 `abs(max_drawdown)`，暂时不会出错，但语义约定冲突。

### 建议修复
1. **统一约定为“回撤幅度非负值”**（推荐）：
   - `max_drawdown` 在系统内部语义定义为 drawdown magnitude（例如 `0.15`）。
2. 在 `parse_backtest_result` 做归一化：
   - `max_drawdown = abs(raw_max_drawdown)`。
3. 在数据类与函数 docstring 明确：
   - “内部统一非负；若平台返回负值会自动取绝对值”。
4. 保留 `abs()` 防御式写法，但注释改为一致语义。
5. 可增加断言/校验：当原始值小于 0 时记录 warning（便于发现上游接口变化）。

---

## 2) 首次迭代是否绕过 max_drawdown 硬约束

- 结论：**部分存在**。
- 对 `autoresearch_joinquant`、`autoresearch_ricequant`：
  - 代码顺序是：先 `validate_result` → 再 `max_drawdown_limit` 检查 → 最后 `champion_metrics is None` 自动 keep。
  - 因此**首次迭代不会绕过**回撤硬约束（你担心的这点在 JQ/RQ 当前实现里不成立）。
- 对 `autoresearch_guorn_strategy`：
  - 当前文件中顺序与 JQ/RQ 一样，也是先检查硬约束，后处理首个版本。
  - 因此“guorn 先判断 champion_metrics is None 再做约束”的描述，与当前代码不一致。

### 建议修复
1. 将决策顺序固化为统一模板（建议抽到公共函数）：
   - `validate` → `hard_constraints` → `first_version_keep` → `score_compare`。
2. 增加单元测试覆盖：
   - `champion=None + drawdown超限` 应返回 rollback。
   - `champion=None + drawdown合格` 应返回 keep。

---

## 3) autoresearch_10jqka_backtest 评分文档与实现偏差 + overfit_penalty 过大

- 结论：**存在**。
- 说明：
  - 顶部注释公式与代码主公式总体一致（包含 `position_penalty` / `overfit_penalty`），但文档未明确“最终得分可为负且理论无下界”。
  - `overfit_penalty = deficit * (5 - max_positions) * 3.0` 未封顶；在低胜率 + 小持仓时惩罚可远大于主项。

### 建议修复
1. 文档补充评分性质：
   - “该评分非归一化分数，可为负，不代表概率或百分比”。
2. 给 `overfit_penalty` 增加上限（推荐）：
   - 方案A：`min(raw_penalty, 1.5)`；
   - 方案B：把惩罚并入权重体系（如单独 weight，默认 0.2）并可配置。
3. 加入数值稳定测试：
   - 验证极端输入不会让惩罚无限放大主项。

---

## 4) `skills/10jqka_backtest/tmp/profile_copy/` 提交了浏览器 profile

- 结论：**存在（高危）**。
- 风险：目录中包含 Cookies / Login Data / History / Session Storage 等典型敏感文件。

### 建议修复（应优先）
1. 立刻从版本库移除并停止跟踪：
   - `git rm -r --cached skills/10jqka_backtest/tmp/profile_copy`
2. 在 `.gitignore` 增加：
   - `skills/10jqka_backtest/tmp/`
   - 或更细粒度：`skills/10jqka_backtest/tmp/profile_copy/`
3. 轮换相关账户凭证/会话（假设已泄露处理）。
4. 若仓库有对外历史，建议做历史清理（`git filter-repo` 或 BFG）并强制重置凭证。

---

## 5) JQ / RQ 大量重复且行为已分叉

- 结论：**存在**。
- 现状：
  - JQ `run_iteration.py` 有 `_load_champion_metrics()`，可优先从 `history` 重建，健壮性更高。
  - RQ 仍直接从 `state.json` 手动拼 `ParsedMetrics`，并把 `total_return` 硬编码为 `0.0`，存在数据缺失风险。

### 建议修复
1. 抽取公共核心模块（建议 `skills/autoresearch_core/`）：
   - `scoring_common.py`（parse/validate/score/decision 基类）；
   - `iteration_common.py`（state/history/champion 重建）；
   - 平台差异仅保留 executor adapter。
2. RQ 对齐 JQ 的 champion 重建策略：
   - 优先 `history/{champion_iter}.json -> fetch_result` 重建；
   - state 仅作 fallback。
3. 补齐 `champion_metrics` 序列化字段：
   - 包含 `total_return`，避免后续指标扩展时踩坑。

---

## 推荐执行优先级

1. **P0（立即）**：清理并阻断 profile 敏感数据。
2. **P1**：统一 `max_drawdown` 内部语义 + 注释/解析归一化。
3. **P1**：给 `overfit_penalty` 加上限并更新文档。
4. **P2**：RQ 对齐 JQ 的 champion 重建逻辑。
5. **P3**：抽公共核心，消除复制粘贴分叉。

---

## 可直接落地的最小改动包（建议）

- `autoresearch_joinquant/scorer.py`、`autoresearch_ricequant/scorer.py`、`autoresearch_guorn_strategy/scorer.py`
  - 统一 `max_drawdown` 文档与注释，parse 时归一化为非负值。
- `autoresearch_10jqka_backtest/scorer.py`
  - 为 `calculate_overfit_penalty` 增加封顶；补充 docstring 说明分数可为负。
- `autoresearch_ricequant/run_iteration.py`
  - 引入 `_load_champion_metrics`（对齐 JQ），去掉 `total_return=0.0` 硬编码。
- `.gitignore`
  - 增加 `skills/10jqka_backtest/tmp/`，并在提交中移除已跟踪 profile 目录。
