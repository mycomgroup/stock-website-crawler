# 任务 14：分钟级与日内策略基线跑通

## 任务目标

把分钟级与日内策略做成第二条基线，明确哪些是真能跑，哪些还只是接口存在。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/minute.py`
- `jqdata_akshare_backtrader_utility/market_api.py`
- `jqdata_akshare_backtrader_utility/timer_rules.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task14_minute_intraday_baseline_result.md`

## 给子 Agent 的提示词

你负责把分钟级和日内策略做成可验证基线。

要求：

- 选取一批真实依赖分钟数据的 txt 策略
- 检查它们是否真实依赖：
  - `1m/5m/15m/30m/60m`
  - `run_daily/open+Nm/HH:MM`
  - `before_open/after_close`
- 跑出一份分钟策略白名单与失败清单
- 对失败原因分类：
  - 数据源缺失
  - timer 语义不一致
  - 竞价/集合竞价能力不足
  - 回测粒度不足

## 任务验证

- 至少跑一批分钟策略样本
- 白名单可复跑
- 对失败分类有明确证据

## 任务成功总结模板

```md
# Task 14 Result

## 修改文件
- ...

## 完成内容
- ...

## 白名单输出
- ...

## 验证方式
- ...

## 已知边界
- ...
```
