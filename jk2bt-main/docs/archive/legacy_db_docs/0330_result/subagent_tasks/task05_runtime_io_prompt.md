# 任务 5：运行时 IO 与观测 API

## 任务目标

补上策略运行时常见的非交易型 API，让依赖这些接口的策略可以在本地继续执行。

## 负责范围

- `jqdata_akshare_backtrader_utility/runtime_io.py`
- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 相关测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task05_runtime_io_result.md`

## 给子 Agent 的提示词

你负责实现本地可用的运行时 IO 与观测 API。请直接编码并补测试。

需要支持或最小可用支持：

- `record`
- `send_message`
- `read_file`
- `write_file`

实现要求：

- `record` 输出到结构化日志或 CSV
- `send_message` 记录到日志，不需要真实发送
- `read_file/write_file` 只能在安全目录内操作，禁止越权访问
- 行为要清楚，失败要明确报错
- 不要为了“模拟云端”而引入复杂服务
- 注意默认运行目录应该在当前 repo 内，不要落到仓库外层

## 任务验证

至少完成以下验证：

- `record` 写出可检查的数据
- `send_message` 有日志落点
- `write_file` 能写
- `read_file` 能读回
- 非法路径会被拒绝

建议命令：

```bash
python3 -m pytest -q tests
```

## 任务成功总结模板

```md
# Task 05 Result

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
