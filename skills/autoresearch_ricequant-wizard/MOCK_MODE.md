# Mock Mode 使用指南

## 概述

Mock Mode 是向导式策略优化系统的离线测试模式，用于在不调用真实 RiceQuant API 的情况下测试整个迭代流程。

## 为什么需要 Mock Mode？

RiceQuant 平台的向导式策略 API 要求 `strategy_id` 必须是整数类型（integer），但 `setup.py` 自动生成的 ID 是字符串格式（如 `wizard_test_fengzhi_value_20260412_101718`）。这导致：

- 无法直接使用自动生成的 ID 进行真实回测
- 需要手动在 RiceQuant 平台创建策略并获取真实 integer ID
- 在获取真实 ID 之前，无法测试迭代流程

Mock Mode 解决了这个问题，允许你在本地完整测试整个优化流程。

## 启用 Mock Mode

### 方法 1：环境变量（推荐）

```bash
export WIZARD_MOCK_MODE=1
python run_iteration.py --base experiments/<name> --mutation-summary "测试变异"
```

### 方法 2：单次命令

```bash
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/<name> \
    --mutation-summary "【add_filter】新增 roe > 10 过滤低质量公司" \
    --mutation-type add_filter
```

## Mock Mode 行为

启用 Mock Mode 后，`wizard_executor.py` 中的以下函数会跳过真实 API 调用：

### 1. `update_strategy()`
- **真实模式**：调用 Node.js run-skill.js 更新 RiceQuant 策略配置
- **Mock 模式**：打印日志，模拟 0.5 秒网络延迟，直接返回

### 2. `run_backtest()`
- **真实模式**：调用 Node.js run-skill.js 触发回测，返回真实 backtest_id
- **Mock 模式**：生成 mock backtest_id（格式：`mock_<timestamp>`），模拟 1 秒提交延迟

### 3. `wait_for_completion()`
- **真实模式**：HTTP 轮询等待回测完成，返回真实指标
- **Mock 模式**：模拟 2 秒回测运行时间，返回随机生成的合理指标

### 4. `fetch_results()`
- **真实模式**：HTTP GET 获取回测结果
- **Mock 模式**：返回与 `wait_for_completion()` 相同的 mock 指标

## Mock 指标生成逻辑

Mock Mode 生成的指标是**随机但合理**的，遵循以下规则：

```python
# 年化收益：8% - 25%
annual_return = random.uniform(0.08, 0.25)

# 最大回撤：与收益相关，但有随机性（收益的 30%-60%）
max_drawdown = abs(annual_return * random.uniform(0.3, 0.6))

# 夏普比率：1.0 - 2.5
sharpe = random.uniform(1.0, 2.5)

# Sortino 通常高于 Sharpe（1.1x - 1.4x）
sortino = sharpe * random.uniform(1.1, 1.4)

# 信息比率：0.5 - 1.5
information_ratio = random.uniform(0.5, 1.5)

# Alpha：年化收益的 30%-70%
alpha = annual_return * random.uniform(0.3, 0.7)

# Beta：0.8 - 1.2
beta = random.uniform(0.8, 1.2)

# 总收益：假设 5 年回测期
total_return = annual_return * 5
```

## 完整测试示例

### 1. 初始化实验（如果尚未初始化）

```bash
python setup.py --name test_mock_mode
```

### 2. 运行多次迭代测试

```bash
# 迭代 1：add_filter
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_mock_mode \
    --mutation-summary "【add_filter】新增 roe > 10" \
    --mutation-type add_filter

# 迭代 2：adjust_holding_num
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_mock_mode \
    --mutation-summary "【adjust_holding_num】maxHoldingNum 15→10" \
    --mutation-type adjust_holding_num

# 迭代 3：adjust_rebalance_interval
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_mock_mode \
    --mutation-summary "【adjust_rebalance_interval】rebalanceInterval 10→20" \
    --mutation-type adjust_rebalance_interval
```

### 3. 查看结果

```bash
# 查看迭代历史
cat experiments/test_mock_mode/history/iterations.tsv

# 查看当前状态
cat experiments/test_mock_mode/state.json

# 查看最新迭代详情
cat experiments/test_mock_mode/history/0002.json
```

## 从 Mock Mode 切换到真实模式

当你准备好使用真实 RiceQuant API 时：

### 1. 在 RiceQuant 平台创建向导式策略

手动在 RiceQuant 平台创建一个向导式策略，获取真实的 integer `strategy_id`（如 `12345678`）。

### 2. 更新 state.json

```bash
# 编辑 experiments/<name>/state.json
# 将 strategy_id 从字符串改为真实 integer ID
{
  "strategy_id": 12345678,  # 改为真实 ID
  ...
}
```

### 3. 关闭 Mock Mode

```bash
# 不设置 WIZARD_MOCK_MODE 环境变量，或设置为 0
unset WIZARD_MOCK_MODE

# 或
export WIZARD_MOCK_MODE=0
```

### 4. 运行真实迭代

```bash
python run_iteration.py \
    --base experiments/<name> \
    --mutation-summary "【add_filter】真实回测测试" \
    --mutation-type add_filter
```

## Mock Mode 的局限性

1. **指标不反映真实市场**：Mock 指标是随机生成的，不代表策略的真实表现
2. **无法验证 API 兼容性**：无法发现 RiceQuant API 的实际问题
3. **无法测试网络异常**：不会遇到超时、连接失败等真实场景

## 适用场景

✅ **适合使用 Mock Mode 的场景：**
- 测试迭代流程是否正常运行
- 验证 keep/rollback 决策逻辑
- 测试 search_notes.md 维护逻辑
- 开发和调试新功能
- 在没有真实 strategy_id 时进行流程验证

❌ **不适合使用 Mock Mode 的场景：**
- 评估策略的真实表现
- 优化真实策略参数
- 生成可用于实盘的配置
- 验证 RiceQuant API 兼容性

## 故障排查

### Q: Mock Mode 下仍然报错 "strategy_id type_error"

A: 检查是否正确设置了环境变量：
```bash
echo $WIZARD_MOCK_MODE  # 应该输出 1
```

### Q: Mock 指标看起来不合理

A: Mock 指标是随机生成的，每次运行都不同。如果需要更真实的指标，请使用真实模式。

### Q: 如何验证 Mock Mode 是否生效？

A: 查看日志输出，应该看到 `[Mock]` 前缀的日志：
```
[Mock] update_strategy: strategy_id=...
[Mock] run_backtest: strategy_id=...
[Mock] wait_for_completion: backtest_id=mock_...
[Mock] fetch_results: strategy_id=...
```

## 总结

Mock Mode 是一个强大的测试工具，让你可以在不依赖真实 RiceQuant API 的情况下完整测试优化流程。在获取真实 strategy_id 之前，建议先使用 Mock Mode 验证整个系统是否正常工作。
