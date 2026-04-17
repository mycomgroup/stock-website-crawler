# Task 27 Result

## 修改文件

- `jqdata_akshare_backtrader_utility/timer_rules.py`
  - 新增 `every_bar` 时间规则
  - 新增 `intraday` 盘中规则
  - 新增 `market_open` / `market_close` 规则
  - 新增中文别名支持：`开盘`、`收盘`、`尾盘`、`盘中`
  - 更新 `check_bar_time_match` 支持新规则类型

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
  - `TimerManager` 新增 `set_data_frequency()` 方法
  - `TimerManager` 新增 `infer_bar_resolution()` 自动推断 bar 粒度
  - `TimerManager._should_execute()` 支持 `every_bar` 规则
  - `JQ2BTBaseStrategy.next()` 在第二个 bar 时自动推断 bar_resolution
  - `run_daily()` 方法改进，正确转发 `every_bar` 参数

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
  - 新增 `_load_minute_data()` 分钟数据加载函数
  - `run_jq_strategy()` 新增 `frequency` 参数支持分钟回测
  - `JQStrategyWrapper` 新增 `frequency` 参数
  - 分钟回测时自动设置 bar_resolution

- `tests/test_minute_replay_engine.py` (新增)
  - 分钟回放引擎单元测试和 smoke test
  - 共 32 个测试用例，覆盖时间规则解析、bar 粒度推断、分钟回放集成等

## 支持的语义

### 时间规则 (time_rule)

| 规则 | 说明 | 示例 |
|------|------|------|
| `every_bar` | 每 bar 触发 | `run_daily(func, time='every_bar')` |
| `open` | 开盘触发 (9:30) | `run_daily(func, time='open')` |
| `before_open` | 开盘前触发 | `run_daily(func, time='before_open')` |
| `after_close` | 收盘后触发 | `run_daily(func, time='after_close')` |
| `HH:MM` | 指定时间触发 | `run_daily(func, time='10:30')` |
| `open+Nm` | 开盘后 N 分钟 | `run_daily(func, time='open+30m')` |
| `open-Nm` | 开盘前 N 分钟 | `run_daily(func, time='open-5m')` |
| `close-Nm` | 收盘前 N 分钟 | `run_daily(func, time='close-10m')` |
| `close+Nm` | 收盘后 N 分钟 | `run_daily(func, time='close+5m')` |
| `market_open` / `开盘` | 开盘触发 | `run_daily(func, time='开盘')` |
| `market_close` / `收盘` / `尾盘` | 收盘触发 | `run_daily(func, time='尾盘')` |
| `intraday` / `盘中` | 仅交易时间触发 | `run_daily(func, time='盘中')` |

### 数据频率

| 频率 | 说明 |
|------|------|
| `daily` | 日线回测（默认） |
| `1m` | 1 分钟回测 |
| `5m` | 5 分钟回测 |
| `15m` | 15 分钟回测 |
| `30m` | 30 分钟回测 |
| `60m` | 60 分钟回测 |

### 核心功能

- **分钟级回放**: 支持分钟数据加载和回测循环
- **every_bar 语义**: 每个 bar 都触发回调
- **bar_resolution 自动推断**: 根据数据自动设置时间粒度
- **时间规则匹配**: 支持 tolerance 机制处理 bar 粒度

## 边界说明

| 语义 | 说明 |
|------|------|
| 精确到秒触发 | 依赖数据源粒度，分钟数据最小粒度为 1 分钟，秒级需秒级数据源 |
| 动态时间规则 | 策略内自行判断即可，如"每突破一次触发"在回调中实现 |
| `close+Nm` | 已支持，回测可正常触发收盘后 N 分钟 |

**注**: API 层面不限制，传入任何时间规则都不会报错，实际触发时机取决于数据粒度。

## 验证样本

### 样本 1: every_bar 测试
```python
# 策略代码
def initialize(context):
    run_daily(handle_bar, time='every_bar')

def handle_bar(context):
    # 每 bar 执行
    pass
```
**结果**: ✅ 通过 - 48 次 bar 触发 48 次回调

### 样本 2: 特定时间触发测试
```python
# 策略代码
def initialize(context):
    run_daily(handle_10_00, time='10:00')

def handle_10_00(context):
    # 10:00 触发
    pass
```
**结果**: ✅ 通过 - 在目标时间附近触发（考虑 bar 粒度 tolerance）

### 样本 3: open+30m 测试
```python
# 时间规则
rule = 'open+30m'
# 预期触发时间: 10:00
```
**结果**: ✅ 通过 - 正确解析为 10:00

### 样本 4: 分钟数据加载测试
```python
# 加载 5 分钟数据
result = run_jq_strategy(
    strategy_file='strategy.txt',
    start_date='2024-01-15',
    end_date='2024-01-18',
    frequency='5m',
    stock_pool=['600519.XSHG']
)
```
**结果**: ✅ 通过 - 数据正确加载并进入回测循环

### 样本 5: 多定时器分钟模式测试
```python
def initialize(context):
    run_daily(every_bar_cb, time='every_bar')
    run_daily(open_cb, time='open')
```
**结果**: ✅ 通过 - `every_bar` 每 bar 触发，`open` 仅开盘时触发

## 已知边界

### 1. 时间匹配 Tolerance 机制
- 当 bar 粒度 > 1 分钟时，时间匹配使用 tolerance 机制
- `tolerance = bar_resolution_minutes`
- 宽松匹配 `tolerance = bar_resolution_minutes * 2`
- 例如：5 分钟 bar，目标 10:00 可能匹配 9:50-10:10 范围

### 2. bar_resolution 自动推断
- 需要至少 2 个 bar 才能推断时间粒度
- 推断发生在第二个 bar
- 如果数据有间隙，推断可能不准确

### 3. 分钟数据源限制
- akshare 分钟数据通常只提供近期数据
- 历史深度有限，不适合长周期回测
- 建议使用 5m 或更大粒度

### 4. 内存使用
- 分钟回测数据量较大
- 建议限制回测时间范围
- 单标的单日约 48 个 5 分钟 bar

### 5. 实盘差异
- 回测中 `every_bar` 严格按 bar 时间触发
- 实盘中 bar 到达时间可能延迟
- 需要考虑实时数据更新时机

## 使用示例

### 基本分钟回测
```python
from jq_strategy_runner import run_jq_strategy

result = run_jq_strategy(
    strategy_file='my_minute_strategy.txt',
    start_date='2024-01-15',
    end_date='2024-01-18',
    frequency='5m',
    stock_pool=['600519.XSHG', '000858.XSHE'],
    initial_capital=100000,
)
```

### 策略中使用 every_bar
```python
def initialize(context):
    g.count = 0
    run_daily(track_price, time='every_bar')

def track_price(context):
    g.count += 1
    price = get_price('600519.XSHG', end_date=context.current_dt, count=1)
    log.info(f'Bar #{g.count}, price: {price}')
```

### 策略中使用特定时间
```python
def initialize(context):
    # 开盘后 30 分钟执行
    run_daily(morning_check, time='open+30m')
    # 收盘前 10 分钟执行
    run_daily(close_position, time='close-10m')

def morning_check(context):
    log.info('开盘后 30 分钟检查')

def close_position(context):
    log.info('收盘前平仓')
```