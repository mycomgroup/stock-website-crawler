# 任务 8：finance 扩展查询

## 任务目标

补 `finance.run_query` 对融资融券、业绩预告、分红表结构保底的支持。

## 负责范围

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要，可拆出 finance 相关辅助模块
- `tests/test_finance_query.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task08_finance_query_result.md`

## 给子 Agent 的提示词

你负责增强 `finance.run_query`，请直接实现和补测试。

重点要求：

- 补齐：
  - `STK_MX_RZ_RQ`
  - `STK_FIN_FORCAST`
- 检查并修复：
  - `STK_XR_XD` 在抓取失败时丢 schema 的问题
- 即使底层网络失败，也尽量返回带稳定列名的空表，而不是完全无列的 `DataFrame`
- 保持当前 query builder 的调用方式不变
- 不要大改 query 语法层，不要顺手重做 ORM

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_finance_query.py
```

建议额外覆盖：

- 分红表至少有 `code`
- 融资融券查询返回稳定字段
- 业绩预告查询返回稳定字段

## 任务成功总结模板

```md
# Task 08 Result

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
