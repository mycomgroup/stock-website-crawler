# 任务 6：竞价与龙虎榜接口

## 任务目标

实现 `get_call_auction` 和 `get_billboard_list` 的真实版或可解释降级版，优先覆盖现有策略高频字段访问。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/`
- 与竞价、龙虎榜直接相关的兼容层代码
- 对应测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/market_data/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task06_call_auction_billboard_result.md`

## 给子 Agent 的提示词

你负责补竞价和龙虎榜接口。请直接落代码，并兼顾字段稳定性和降级可解释性。

具体要求：

- 实现：
  - `get_call_auction`
  - `get_billboard_list`
- 返回 `DataFrame`
- 列名尽量稳定，优先兼容现有策略访问习惯
- 如果底层源数据无法获取，不能静默返回莫名其妙的空值
- 可以降级返回空表，但必须：
  - 保留稳定 schema
  - 打印或记录清晰告警
- 不要把这个任务扩展到资金流或 finance

## 任务验证

至少完成以下验证：

- 竞价接口返回结构稳定
- 龙虎榜接口返回结构稳定
- 无数据或离线时，仍能返回带 schema 的空表

建议命令：

```bash
python3 -m pytest -q tests
```

## 任务成功总结模板

```md
# Task 06 Result

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
