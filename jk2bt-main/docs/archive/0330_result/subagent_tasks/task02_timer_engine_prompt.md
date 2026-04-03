# 任务 2：Timer 规则引擎

## 任务目标

替换当前过于简化的定时器逻辑，实现更接近聚宽语义的规则判断。

## 负责范围

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要，可新增定时规则辅助模块
- `tests/test_timer_mechanism.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task02_timer_engine_result.md`

## 给子 Agent 的提示词

你负责把当前过于简化的 Timer 逻辑改成真正可用的规则引擎。请直接实现，不要只停留在方案说明。

具体要求：

- 支持：
  - `run_daily`
  - `run_weekly`
  - `run_monthly`
- 支持时间规则：
  - `before_open`
  - `open`
  - `after_close`
  - `HH:MM`
  - `open+30m`
- 支持基础日期规则：
  - 周几
  - 月内第 N 个交易日
  - 避免同一交易日重复触发
- 尽量纯函数化，方便单测。
- 若 Backtrader 粒度不足以精确模拟某些时间点，允许降级，但必须显式说明，不要假装精确支持。
- 不要顺手改订单系统或行情模块。

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_timer_mechanism.py
```

建议补充：

- daily/weekly/monthly 基础触发测试
- 同一日不重复触发测试
- `open+30m` 与固定时刻 `HH:MM` 测试

## 任务成功总结模板

```md
# Task 02 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证命令
```bash
...
```

## 验证结果
- ...

## 已知边界
- ...
```
