# Mock Mode 快速开始

## 一分钟上手

### 1. 运行单次迭代

```bash
cd skills/autoresearch_ricequant-wizard

WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【add_filter】新增 roe > 10" \
    --mutation-type add_filter
```

### 2. 查看结果

```bash
# 查看最新迭代
tail -5 experiments/test_fengzhi_value/history/iterations.tsv

# 查看当前状态
cat experiments/test_fengzhi_value/state.json | grep -E "champion_score|champion_iter|consecutive_failures"
```

### 3. 运行多次迭代

```bash
# 迭代 1
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【add_filter】新增 roe > 10" \
    --mutation-type add_filter

# 迭代 2
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【adjust_holding_num】maxHoldingNum 15→10" \
    --mutation-type adjust_holding_num

# 迭代 3
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【adjust_rebalance_interval】rebalanceInterval 10→20" \
    --mutation-type adjust_rebalance_interval
```

## 可用的变异类型

| mutation-type | 说明 | 示例 |
|---------------|------|------|
| `add_filter` | 新增筛选条件 | 新增 roe > 10 |
| `remove_filter` | 删除筛选条件 | 删除 debt_ratio < 50 |
| `adjust_filter_threshold` | 调整筛选阈值 | pe_ratio 15→12 |
| `add_sorting` | 新增排序规则 | 新增 roe 降序 |
| `adjust_sorting_weight` | 调整排序权重 | dividend_yield 0.6→0.8 |
| `adjust_holding_num` | 调整持仓数量 | maxHoldingNum 15→10 |
| `adjust_rebalance_interval` | 调整调仓周期 | rebalanceInterval 10→20 |
| `change_universe` | 切换股票池 | 000300→000905 |

## 常用命令

### 查看迭代历史
```bash
cat experiments/test_fengzhi_value/history/iterations.tsv | column -t -s $'\t'
```

### 查看最新迭代详情
```bash
# 替换 0006 为实际迭代编号
cat experiments/test_fengzhi_value/history/0006.json | python -m json.tool
```

### 查看当前配置
```bash
cat experiments/test_fengzhi_value/wizard_config.json | python -m json.tool
```

### 查看搜索地图
```bash
cat experiments/test_fengzhi_value/history/search_notes.md
```

## 预期输出

### 成功的 keep 输出
```
[iter_0006] 开始迭代 strategy_id=wizard_test_fengzhi_value_20260412_101718
[iter_0006] 执行变异 mutation_type=adjust_holding_num
[iter_0006] 变异描述: adjust_holding_num: 15 -> 10
[Mock] update_strategy: strategy_id=...
[Mock] run_backtest: strategy_id=..., backtest_id=mock_1775960997
[Mock] wait_for_completion: backtest_id=mock_1775960997
[Mock] fetch_results: strategy_id=...
[iter_0006] score=1.8957 champion=1.8508 annual=13.42% dd=7.21% sharpe=1.60 sortino=2.64
[iter_0006] 决策: keep — new_score 1.895722 > champion_score 1.850825 (diff: 0.044897)
[iter_0006] ✅ keep — 新 champion iter=0006 score=1.8957

Exit Code: 0
```

### 成功的 rollback 输出
```
[iter_0007] score=1.7234 champion=1.8957 annual=10.23% dd=8.45% sharpe=1.21 sortino=2.10
[iter_0007] 决策: rollback — new_score 1.723400 <= champion_score 1.895722 (diff: -0.172322)
[iter_0007] ↩️  rollback — new_score 1.723400 <= champion_score 1.895722 (diff: -0.172322)

Exit Code: 1
```

## 验证 Mock Mode 是否生效

查看日志中是否有 `[Mock]` 前缀：

```bash
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "测试" \
    --mutation-type add_filter 2>&1 | grep "\[Mock\]"
```

应该看到：
```
[Mock] update_strategy: strategy_id=...
[Mock] run_backtest: strategy_id=...
[Mock] wait_for_completion: backtest_id=mock_...
[Mock] fetch_results: strategy_id=...
```

## 故障排查

### Q: 没有看到 [Mock] 日志

**A**: 检查环境变量是否正确设置：
```bash
echo $WIZARD_MOCK_MODE  # 应该输出 1
```

如果输出为空或 0，重新设置：
```bash
export WIZARD_MOCK_MODE=1
```

### Q: 仍然报错 "strategy_id type_error"

**A**: 确认使用了环境变量：
```bash
# 错误（没有环境变量）
python run_iteration.py --base experiments/test_fengzhi_value --mutation-summary "测试"

# 正确（有环境变量）
WIZARD_MOCK_MODE=1 python run_iteration.py --base experiments/test_fengzhi_value --mutation-summary "测试"
```

### Q: Mock 指标看起来不合理

**A**: Mock 指标是随机生成的，每次运行都不同。这是正常的，Mock Mode 的目的是测试流程，不是评估策略真实表现。

## 下一步

### 继续测试
运行更多迭代，观察 keep/rollback 决策：
```bash
for i in {1..10}; do
    WIZARD_MOCK_MODE=1 python run_iteration.py \
        --base experiments/test_fengzhi_value \
        --mutation-summary "【测试】迭代 $i"
    echo "---"
done
```

### 切换到真实模式
1. 在 RiceQuant 平台创建向导式策略，获取真实 integer strategy_id
2. 更新 `experiments/test_fengzhi_value/state.json` 中的 `strategy_id`
3. 关闭 Mock Mode：`unset WIZARD_MOCK_MODE`
4. 运行真实迭代

## 更多信息

- 详细使用指南：[MOCK_MODE.md](./MOCK_MODE.md)
- 测试报告：[experiments/test_fengzhi_value/MOCK_TEST_REPORT.md](./experiments/test_fengzhi_value/MOCK_TEST_REPORT.md)
- 完整总结：[TASK_COMPLETION_SUMMARY.md](./TASK_COMPLETION_SUMMARY.md)
