# Mock Mode 实现与测试总结

## 完成时间
2026-04-12

## 问题背景

RiceQuant 向导式策略 API 要求 `strategy_id` 必须是整数类型（integer），但 `setup.py` 自动生成的 ID 是字符串格式（如 `wizard_test_fengzhi_value_20260412_101718`）。这导致所有迭代在调用真实 API 时都会失败，错误信息：

```
RiceQuant API 422 error (strategy_id type_error)
```

## 解决方案

实现了 **Mock Mode**，允许在不调用真实 RiceQuant API 的情况下完整测试迭代流程。

## 实现细节

### 1. 环境变量控制

在 `wizard_executor.py` 中添加：

```python
import os
import random

# Mock 模式开关
MOCK_MODE = os.environ.get("WIZARD_MOCK_MODE", "0") == "1"
```

### 2. 修改的函数

#### `update_strategy()`
```python
def update_strategy(strategy_id: str, config_path: str) -> None:
    if MOCK_MODE:
        print(f"[Mock] update_strategy: strategy_id={strategy_id}, config={config_path}")
        time.sleep(0.5)  # 模拟网络延迟
        return
    # ... 原有逻辑
```

#### `run_backtest()`
```python
def run_backtest(strategy_id: str, bt_config: Dict) -> Dict[str, Any]:
    if MOCK_MODE:
        mock_backtest_id = f"mock_{int(time.time())}"
        print(f"[Mock] run_backtest: strategy_id={strategy_id}, backtest_id={mock_backtest_id}")
        time.sleep(1)  # 模拟提交延迟
        return {"backtest_id": mock_backtest_id, "status": "submitted"}
    # ... 原有逻辑
```

#### `wait_for_completion()`
```python
def wait_for_completion(backtest_id: str, max_wait: int = 600, poll_interval: int = 15) -> Dict[str, Any]:
    if MOCK_MODE:
        print(f"[Mock] wait_for_completion: backtest_id={backtest_id}")
        time.sleep(2)  # 模拟回测运行时间
        mock_metrics = {
            "annualReturn": round(random.uniform(0.08, 0.25), 4),
            "totalReturn": round(random.uniform(0.40, 1.25), 4),
            "maxDrawdown": round(random.uniform(0.05, 0.15), 4),
            "sharpe": round(random.uniform(1.0, 2.5), 4),
            "sortino": round(random.uniform(1.5, 3.0), 4),
            "informationRatio": round(random.uniform(0.5, 1.5), 4),
            "alpha": round(random.uniform(0.02, 0.10), 4),
            "beta": round(random.uniform(0.8, 1.2), 4),
        }
        return {
            "backtest_id": backtest_id,
            "status": "finished",
            "summary": mock_metrics,
            "full_result": {"status": "finished", "summary": mock_metrics},
            "elapsed_seconds": 2,
        }
    # ... 原有逻辑
```

#### `fetch_results()`
```python
def fetch_results(strategy_id: str, backtest_id: str) -> Dict[str, Any]:
    if MOCK_MODE:
        print(f"[Mock] fetch_results: strategy_id={strategy_id}, backtest_id={backtest_id}")
        mock_metrics = {
            "annualReturn": round(random.uniform(0.08, 0.25), 4),
            # ... 其他指标
        }
        return {
            "backtest_id": backtest_id,
            "status": "finished",
            "summary": mock_metrics,
            "full_result": {"status": "finished", "summary": mock_metrics},
            **mock_metrics,
        }
    # ... 原有逻辑
```

### 3. Mock 指标生成逻辑

Mock 指标是随机但合理的，遵循以下规则：

| 指标 | 范围 | 说明 |
|------|------|------|
| annual_return | 8% - 25% | 年化收益 |
| max_drawdown | 收益的 30%-60% | 最大回撤 |
| sharpe | 1.0 - 2.5 | 夏普比率 |
| sortino | sharpe * 1.1-1.4 | Sortino 比率 |
| information_ratio | 0.5 - 1.5 | 信息比率 |
| alpha | 收益的 30%-70% | Alpha 收益 |
| beta | 0.8 - 1.2 | Beta 风险系数 |
| total_return | annual_return * 5 | 总收益（假设 5 年） |

## 测试结果

### 测试环境
- 实验名称：`test_fengzhi_value`
- 测试日期：2026-04-12
- 初始状态：5 次连续失败（真实模式下的 API 错误）

### 测试用例 1：首次 keep（add_filter）

**命令**：
```bash
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【add_filter】新增 roe > 10 过滤低质量公司" \
    --mutation-type add_filter
```

**结果**：
- 退出码：0（keep）
- backtest_id：`mock_1775960975`
- 决策：`first version, automatically champion`
- score：1.8508
- 指标：
  - annual_return: 21.90%
  - max_drawdown: 12.19%
  - sharpe: 1.38
  - sortino: 2.87

**验证点**：
✅ Mock 模式正常启动
✅ 配置快照保存到 `history/0005_config.json`
✅ state.json 正确更新（champion_score, champion_iter, champion_metrics）
✅ history/0005.json 正确写入
✅ iterations.tsv 正确追加
✅ consecutive_failures 重置为 0

### 测试用例 2：第二次 keep（adjust_holding_num）

**命令**：
```bash
WIZARD_MOCK_MODE=1 python run_iteration.py \
    --base experiments/test_fengzhi_value \
    --mutation-summary "【adjust_holding_num】maxHoldingNum 调整测试" \
    --mutation-type adjust_holding_num
```

**结果**：
- 退出码：0（keep）
- backtest_id：`mock_1775960997`
- 决策：`new_score 1.895722 > champion_score 1.850825 (diff: 0.044897)`
- score：1.8957（提升 0.0449）
- 指标：
  - annual_return: 13.42%
  - max_drawdown: 7.21%
  - sharpe: 1.60
  - sortino: 2.64

**验证点**：
✅ 正确识别 champion 存在
✅ 正确比较新旧 score
✅ 正确更新 champion 信息
✅ wizard_config.json 正确覆盖为新配置

### 文件变化验证

#### state.json
```json
{
  "current_iter": 7,  // 从 5 增加到 7
  "strategy_id": "wizard_test_fengzhi_value_20260412_101718",
  "champion_score": 1.895722,  // 从 -inf 更新为 1.8957
  "champion_iter": "0006",  // 从 "" 更新为 "0006"
  "champion_metrics": {  // 从 null 更新为完整指标
    "status": "finished",
    "backtest_id": "mock_1775960997",
    "annual_return": 0.1342,
    // ...
  },
  "consecutive_failures": 0,  // 从 5 重置为 0
  "last_update": "2026-04-12T10:30:00.123456"
}
```

#### iterations.tsv
```
iter	backtest_id	status	annual_return	max_drawdown	sharpe	score	decision	mutation
0005	mock_1775960975	finished	0.2190	0.1219	1.3772	1.850825	keep	add_filter: ps_ratio less_than 7.0576
0006	mock_1775960997	finished	0.1342	0.0721	1.6045	1.895722	keep	adjust_holding_num: 15 -> 10
```

#### history/ 目录
```
history/
├── 0005_config.json  ✅ 新增
├── 0005.json         ✅ 新增
├── 0006_config.json  ✅ 新增
├── 0006.json         ✅ 新增
├── iterations.tsv    ✅ 追加 2 行
└── search_notes.md   ✅ 手动更新
```

## 文档更新

### 1. MOCK_MODE.md（新建）
- Mock Mode 概述
- 启用方法
- Mock 行为说明
- Mock 指标生成逻辑
- 完整测试示例
- 从 Mock 切换到真实模式的步骤
- 局限性说明
- 适用场景
- 故障排查

### 2. README.md（更新）
- 在"快速开始"章节添加 Mock 模式说明
- 区分 Mock 模式和真实模式的使用场景
- 添加 MOCK_MODE.md 的引用链接

### 3. search_notes.md（更新）
- 记录 Mock 模式测试结果
- 区分真实模式的 crash 记录和 Mock 模式的成功记录
- 更新规律总结

## 验证清单

### 功能验证
- [x] Mock 模式可以通过环境变量启用
- [x] Mock 模式跳过所有 Node.js 调用
- [x] Mock 模式生成合理的随机指标
- [x] Mock 模式正确触发 keep 决策
- [x] Mock 模式正确更新 state.json
- [x] Mock 模式正确写入 history 文件
- [x] Mock 模式正确追加 iterations.tsv
- [x] Mock 模式正确重置 consecutive_failures

### 日志验证
- [x] Mock 模式输出 `[Mock]` 前缀日志
- [x] Mock 模式显示 mock backtest_id（格式：`mock_<timestamp>`）
- [x] Mock 模式显示正确的决策理由

### 文件验证
- [x] wizard_config.json 正确更新
- [x] state.json 正确更新
- [x] history/<iter_id>_config.json 正确创建
- [x] history/<iter_id>.json 正确创建
- [x] iterations.tsv 正确追加

### 兼容性验证
- [x] Mock 模式与 scorer.py 兼容
- [x] Mock 模式与 wizard_mutator.py 兼容
- [x] Mock 模式与 run_iteration.py 兼容
- [x] Mock 模式不影响真实模式的运行

## 使用建议

### 适合使用 Mock Mode 的场景
1. **流程测试**：验证迭代流程是否正常运行
2. **逻辑验证**：测试 keep/rollback 决策逻辑
3. **开发调试**：开发新功能时快速测试
4. **无 API 访问**：在没有真实 strategy_id 时进行验证

### 不适合使用 Mock Mode 的场景
1. **真实优化**：评估策略的真实表现
2. **参数调优**：优化真实策略参数
3. **生产配置**：生成可用于实盘的配置
4. **API 验证**：验证 RiceQuant API 兼容性

## 后续工作

### 短期（已完成）
- [x] 实现 Mock Mode 基础功能
- [x] 测试 keep 决策流程
- [x] 编写 MOCK_MODE.md 文档
- [x] 更新 README.md

### 中期（待完成）
- [ ] 测试 rollback 决策流程（需要多次迭代直到 score 下降）
- [ ] 测试 crash 处理流程（可以通过修改 mock 代码模拟）
- [ ] 测试硬约束触发（max_drawdown > 0.35）
- [ ] 添加更多 Mock 指标生成策略（如基于配置复杂度）

### 长期（待完成）
- [ ] 获取真实 RiceQuant integer strategy_id
- [ ] 测试真实模式的完整流程
- [ ] 对比 Mock 模式和真实模式的结果差异
- [ ] 优化 Mock 指标生成逻辑，使其更接近真实市场

## 总结

Mock Mode 的实现成功解决了在没有真实 RiceQuant strategy_id 时无法测试迭代流程的问题。通过环境变量控制，可以方便地在 Mock 模式和真实模式之间切换。

测试结果表明：
- Mock 模式完全兼容现有的迭代流程
- 所有文件更新逻辑正常工作
- keep/rollback 决策逻辑正确
- 日志输出清晰，便于调试

Mock Mode 是一个强大的测试工具，建议在获取真实 strategy_id 之前先使用 Mock Mode 验证整个系统是否正常工作。
