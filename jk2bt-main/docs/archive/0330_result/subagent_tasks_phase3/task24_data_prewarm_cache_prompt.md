# 任务 24：数据预热与缓存闭环

## 任务目标

建立可复用的数据预热和缓存闭环，减少日线策略因网络不稳定而失败。

## 负责范围

- `jqdata_akshare_backtrader_utility/db/`
- `jqdata_akshare_backtrader_utility/market_data/`
- 仓库根目录的数据预热脚本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/db/`
  - `jqdata_akshare_backtrader_utility/market_data/`
  - 仓库根目录
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task24_data_prewarm_cache_result.md`

## 给子 Agent 的提示词

你负责把日线数据、元数据、常用基础面数据做成可预热缓存闭环。

要求：

- 设计并落地预热流程：
  - 股票/ETF 日线
  - 交易日历
  - 证券基础信息
  - 常见基础面/估值所需数据
- 支持指定股票池和时间范围
- 支持“缓存已存在则跳过”
- 优先保证 `run_jq_strategy(..., use_cache_only=True)` 这类模式可用
- 输出缓存范围说明，不要让使用者误以为“离线模式支持全部市场全部时间”

## 任务验证

- 至少预热一个固定时间区间和样本股票池
- 用缓存模式跑至少一个真实策略

## 任务成功总结模板

```md
# Task 24 Result

## 修改文件
- ...

## 预热内容
- ...

## 验证样本
- ...

## 验证方式
- ...

## 已知边界
- ...
```
