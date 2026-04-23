# Entry Overlay 产品文档（V1）

## 1. 产品定位

Entry Overlay 是“策略执行层增强组件”。

- 输入：原策略给出的候选标的与买入信号。
- 输出：买入评分、是否执行、候选最佳买点时刻。
- 范围：只增强买点时序，不替代原有 alpha 选股逻辑。

## 2. 关键场景

### 场景 A：排序过滤（rank_filter）

用于每日/每周选股后最后排序：
- 对每个候选标的计算 `entry_score`
- 根据分数重排或设置阈值过滤
- 优先执行高分标的

### 场景 B：必须买仅择时（timing_only）

信号已确定必须买入：
- 不再判断买不买
- 返回候选时点 `best_times`
- 在一周内挑最优时点成交

## 3. 功能清单

- 15 技术因子计算（TA-Lib + fallback）
- Profile 模板：`general` / `trend` / `reversal`
- 数据适配：JoinQuant / Akshare / Pandas
- 事件回测：`run_event_backtest`
- 参数搜索：`grid_search_params`
- CLI 脚本：`python -m entry_overlay.run_offline_validation`

## 4. 非功能要求

- **可插拔**：原策略仅在买入前调用 `engine.decide()`。
- **可回滚**：关闭 overlay 后回到原交易行为。
- **可验证**：先离线回测，再灰度上线。
- **可复用**：跨策略共享同一组件。

## 5. 上线流程建议

1. 选 1 条主策略灰度接入。
2. 离线跑 3 套 profile + 4 个阈值网格。
3. 在线 A/B 对比（至少 4 周）。
4. 达标后复制到其余策略。

## 6. 版本边界

V1 只做买点增强，不改卖出逻辑。
后续 V2 可增加卖点 overlay 与成交成本建模。
