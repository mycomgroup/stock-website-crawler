# Task 02 Result: Timer 规则引擎

## 修改文件

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/timer_rules.py`（已有，未修改）
- `tests/test_timer_mechanism.py`
- `tests/test_timer_rules.py`（已有，未修改）

## 完成内容

### 1. TimerManager 简化逻辑改进

改进了 `TimerManager._should_execute` 方法的简化逻辑（当 `timer_rules` 模块不可用时的备用方案）：

- **weekly 触发改进**：使用 `week_start` 精确判断是否同一周，而非简单的 `days // 7`
- **monthly 触发改进**：支持 `day` 参数（月内第 N 个交易日），使用 `_get_nth_trading_day` 计算
- **时间规则支持**：添加 `_check_time_rule` 方法，支持 `before_open`, `open`, `after_close`, `HH:MM`, `open+Nm`, `open-Nm` 等时间规则
- **周末过滤**：直接在简化逻辑中过滤周末

### 2. 新增辅助方法

- `_check_time_rule(bar_time, time_rule)`：检查时间规则匹配
- `_get_nth_trading_day(year, month, n)`：获取月内第 N 个交易日（简化版，仅排除周末）

### 3. 测试补充

新增 `TestTimerTimeRules` 和 `TestTimerDayRules` 测试类，覆盖：

**时间规则测试：**
- `open+30m` 时间规则匹配
- `HH:MM` 固定时间规则匹配
- `before_open` 时间规则匹配
- `after_close` 时间规则匹配
- `open-5m` 时间规则匹配
- 带时间规则的定时器不重复触发

**日期规则测试：**
- 月内第一个交易日触发
- 月内最后一个交易日触发
- 周几触发
- 同一周不重复触发
- 周末不是交易日

## 验证命令

```bash
python3 -m pytest -q tests/test_timer_mechanism.py tests/test_timer_rules.py
```

## 验证结果

```
tests/test_timer_mechanism.py: 28 passed
tests/test_timer_rules.py: 56 passed
Total: 84 passed
```

## 支持的规则

### 频率规则

| 规则 | 说明 |
|------|------|
| `run_daily` | 每个交易日执行一次 |
| `run_weekly` | 每周执行一次（指定周几） |
| `run_monthly` | 每月执行一次（指定月内第 N 个交易日） |

### 时间规则

| 规则 | 说明 |
|------|------|
| `before_open` | 开盘前（9:30 之前） |
| `open` | 开盘时（9:30） |
| `after_close` | 收盘后（15:00 及之后） |
| `HH:MM` | 固定时间，如 `10:30` |
| `open+Nm` | 开盘后 N 分钟，如 `open+30m` |
| `open-Nm` | 开盘前 N 分钟，如 `open-5m` |

### 日期规则

| 规则 | 说明 |
|------|------|
| `weekday=N` | 周几执行（1=周一, 5=周五） |
| `day=N` | 月内第 N 个交易日（1=第一个, -1=最后一个） |

## 已知边界

1. **时间粒度限制**：Backtrader 日线回测时，bar 时间默认为 00:00，时间规则会降级为"跳过时间检查"。需使用分钟数据才能精确匹配时间规则。

2. **节假日处理**：简化逻辑仅排除周末，不处理节假日。建议提供完整交易日历（`trading_days` 参数）以获得精确判断。`timer_rules` 模块在导入成功时会使用完整交易日历。

3. **bar 粒度匹配**：时间匹配允许 `bar_resolution_minutes` 范围内的误差。若 bar 粒度较粗（如 30 分钟），精确时间点可能无法匹配，会降级为宽松匹配并发出警告。

4. **简化逻辑备用**：`timer_rules` 模块是主要实现，简化逻辑仅作为备用方案。若 `timer_rules` 可用，将优先使用其完整实现。